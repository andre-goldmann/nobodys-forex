package jdg.digital.forexbackend.domain;

import jdg.digital.api_interface.StrategyEnum;
import jdg.digital.api_interface.SymbolEnum;
import jdg.digital.api_interface.Trade;
import jdg.digital.api_interface.TradeTypeEnum;
import jdg.digital.forexbackend.domain.model.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import static jdg.digital.forexbackend.domain.model.StrategyNameMapping.STRATEGY_NAMES;

@Service
@Slf4j
public class TradesService {

    @Autowired
    private TradeRepository tradeRepository;

    public Mono<List<Trade>> getTradesWithPositiveProfit(final SymbolEnum symbolEnum, final StrategyEnum strategyEnum) {
        log.info("Search for {}-{}", symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum));
        return this.tradeRepository.loadTrades(symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum))
                .map(this::entityToDto).collectList();
    }

    public Mono<List<Trade>> getTradesWithNegativeProfit(final SymbolEnum symbolEnum, final StrategyEnum strategyEnum) {
        log.info("Search for {}-{}", symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum));
        return this.tradeRepository.loadTrades(symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum))
                .map(this::entityToDto).collectList();
    }

    private Trade entityToDto(final TradesEntity entity) {
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
            if(entity.getProfit() != null && entity.getCommision() != null && entity.getSwap() != null) {
                final BigDecimal profit = BigDecimal.valueOf(entity.getProfit() - entity.getCommision() -  entity.getSwap());
                trade.setProfit(profit.setScale(2, RoundingMode.HALF_UP).doubleValue());
            }

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


}
