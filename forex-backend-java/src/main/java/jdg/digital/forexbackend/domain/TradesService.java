package jdg.digital.forexbackend.domain;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.forexbackend.domain.model.*;
import jdg.digital.forexbackend.interfaces.ForexProducerService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import static jdg.digital.forexbackend.domain.model.StrategyNameMapping.STRATEGY_NAMES;

@Service
@Slf4j
public class TradesService {

    @Autowired
    private TradeRepository tradeRepository;

    @Autowired
    private ProdTradeRepository prodTradeRepository;

    @Autowired
    private ForexProducerService forexProducerService;

    public Mono<List<Trade>> getTradesWithPositiveProfit(final SymbolEnum symbolEnum, final StrategyEnum strategyEnum) {
        log.info("Search for {}-{}", symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum));
        return Mono.fromCallable(
                () -> this.tradeRepository.loadTrades(symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum)).stream()
                .filter(e -> e.getProfit() > 0)
                .map(this::entityToDto)
                .toList());
    }

    public Mono<List<Trade>> getTradesWithNegativeProfit(final SymbolEnum symbolEnum, final StrategyEnum strategyEnum) {
        log.info("Search for {}-{}", symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum));
        return Mono.fromCallable(
                () -> this.tradeRepository.loadTrades(symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum)).stream()
                .filter(e -> e.getProfit() < 0)
                .map(this::entityToDto)
                .toList());
    }

    public Mono<List<Trade>> getWaitingTrades(String env) {
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> Mono.fromCallable(
                    () -> this.tradeRepository.waitingTradesDev().stream()
                            .map(this::entityToDto)
                            .toList());
            case "PROD" -> Mono.fromCallable(
                    () -> this.tradeRepository.waitingTradesProd().stream()
                            .map(this::entityToDto)
                            .toList());
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };

    }

    private Trade entityToDto(final TradesEntity entity) {
        log.info(entity.toString());
        final Trade trade = new Trade();
        trade.setSymbol(SymbolEnum.fromValue(entity.getSymbol()));
        final Set<StrategyEnum> strategies = STRATEGY_NAMES.entrySet().stream()
                .filter(entry -> entry.getValue().equals(entity.getStrategy()))
                .map(Map.Entry::getKey)
                .collect(Collectors.toSet());
        if(strategies.isEmpty()){
            throw new IllegalArgumentException("Not StrategyEnum found for " + entity.getStrategy());
        } else if (strategies.size() > 1){
            throw new IllegalArgumentException("Multiple StrategyEnums found for " + entity.getStrategy());

        }
        trade.setStrategy(strategies.stream().findFirst().get());
        trade.setExit(entity.getExit());
        trade.setEntry(entity.getEntry());
        final BigDecimal profit = BigDecimal.valueOf(entity.getProfit() - entity.getCommision() -  entity.getSwap());
        trade.setProfit(profit.setScale(2, RoundingMode.HALF_UP).doubleValue());
        if(entity.getClosed() != null && !entity.getClosed().isEmpty()) {
            final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy.MM.dd HH:mm");
            final LocalDateTime localDateTime = LocalDateTime.parse(entity.getClosed(), formatter);
            trade.setClosed(localDateTime.atOffset(ZoneOffset.UTC));
        }
        if(entity.getActivated() != null && !entity.getActivated().isEmpty()) {
            final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy.MM.dd HH:mm:ss");
            final LocalDateTime localDateTime = LocalDateTime.parse(entity.getActivated(), formatter);
            trade.setActivated(localDateTime.atOffset(ZoneOffset.UTC));
        }
        trade.setType(TradeTypeEnum.valueOf(entity.getType().toUpperCase()));
        return trade;
    }

    public Mono<Trade> updateTrade(String env, Trade trade) {
        System.out.println("Update trade " + trade.toString());
        return Mono.empty();
    }

    @Transactional
    public String storeSignal(final Signal signal, final TradeStat stats) {
        log.info("Signal {} has stats {}", signal, stats);

        final Integer activeTrades = this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy());
        if(activeTrades < 4) {
            this.prodTradeRepository.insertProdTradeEntity(
                    signal.symbol(),
                    signal.type(),
                    signal.entry(),
                    signal.sl(),
                    signal.tp(),
                    0.01,
                    signal.strategy(),
                    LocalDateTime.now());
            try {
                this.forexProducerService.sendMessage("signals", new ObjectMapper().writeValueAsString(signal));
            } catch (JsonProcessingException e) {
                log.error("Error sending signal to queue", e);
                throw new RuntimeException(e);
            }
        } else {
            try {
                // {"symbol":"EURCHF","timestamp":"signal.timestamp","type":"sell","entry":1.0,"sl":1.0,"tp":1.0,"strategy":"VHMA_WITHOUT_REG"}
                final String ignored ="{\"message\":\"Ignore because there more then " + activeTrades + " active trade\"," + new ObjectMapper().writeValueAsString(signal) + "}";
                this.forexProducerService.sendMessage("signals", ignored);
            } catch (JsonProcessingException e) {
                log.error("Error sending signal to queue", e);
                throw new RuntimeException(e);
            }
        }

        return "Signal processed";
    }
}
