package jdg.digital.forexbackend.domain;

import jdg.digital.forexbackend.domain.model.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import static jdg.digital.forexbackend.domain.model.StrategyNameMapping.STRATEGY_NAMES;

@Service
@Slf4j
public class TradeStatsServices {

    public static final double WIN_PERCENTAGE = 62.0;
    public static final double MIN_PROFIT = 10.0;
    public static final int MIN_TRADES = 150;

    @Autowired
    private TradeStatsRepository tradeStatsRepository;

    @Autowired
    private SignalRepository signalRepository;

    // TODO change return to Mono<>
    public Mono<List<TradeStat>> getTradeStats(final String env) {

        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> Mono.fromCallable(
                    () -> this.tradeStatsRepository.statsDevTrades(MIN_TRADES, MIN_PROFIT, WIN_PERCENTAGE)
                            .stream()
                            .map(this::mapToTrade)
                            .toList()
            );
            case "PROD" -> Mono.fromCallable(
                    () -> this.tradeStatsRepository.statsProdTrades()
                            .stream()
                            .map(this::mapToTrade)
                            .toList()
            );
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
    }

    public Mono<TradeStat> getStatsFor(final Signal signal) {
        return Mono.fromCallable(() -> {
            final TradeStatInterface entity = this.tradeStatsRepository.getStatsFor(signal.symbol(), signal.strategy());
            if(entity == null){
                log.warn("Stats not found Signal of {}-{}", signal.symbol(), signal.strategy());
                this.signalRepository.insertDevTradeEntity(
                        signal.symbol(),
                        signal.type(),
                        signal.entry(),
                        signal.sl(),
                        signal.tp(),
                        signal.lots(),
                        signal.strategy(),
                        LocalDateTime.now());

                return null;
            }
            return mapToTrade(entity);
        });
    }

    private TradeStat mapToTrade(final TradeStatInterface entity) {
        if(entity.getSymbol() == null || entity.getSymbol().isEmpty() || entity.getStrategy() == null || entity.getStrategy().isEmpty()){
            throw new IllegalArgumentException("Symbol or strategy is null/empty");
        }
        final TradeStat stat = new TradeStat();
        stat.setSymbol(SymbolEnum.fromValue(entity.getSymbol()));

        final Set<StrategyEnum> strategies = STRATEGY_NAMES.entrySet().stream()
                .filter(entry -> entry.getValue().equals(entity.getStrategy()))
                .map(Map.Entry::getKey)
                .collect(Collectors.toSet());
        if(strategies.isEmpty()){
            throw new IllegalArgumentException("Not StrategyEnum found for " + entity.getStrategy());
        } else if (strategies.size() > 1){
            throw new IllegalArgumentException("Multiple StrategyEnums found for " + entity.getStrategy());

        }
        stat.setStrategy(strategies.stream().findFirst().get());
        // get StrategyEnum from StrategyNameMapping using entity.getStrategy()

        stat.setProfit(BigDecimal.valueOf(entity.getProfit()).setScale(2, RoundingMode.HALF_UP).doubleValue());
        stat.setLoses(entity.getLoses());
        stat.setTotal(entity.getTotal());
        stat.setWins(entity.getWins());
        stat.setWinpercentage(entity.getWinPercentage());
        return stat;
    }
}
