package jdg.digital.forexbackend.domain;

import jdg.digital.api_interface.*;
import jdg.digital.forexbackend.domain.model.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.*;
import java.util.stream.Collectors;
import static jdg.digital.forexbackend.domain.model.StrategyNameMapping.STRATEGY_NAMES;

@Service
@Slf4j
public class TradeStatsServices {

    public static final double WIN_PERCENTAGE = 63.0;
    public static final double MIN_PROFIT = 10.0;
    public static final int MIN_TRADES = 150;

    @Autowired
    private TradeStatsRepository tradeStatsRepository;

    @Autowired
    private ProdTradeRepository prodTradeRepository;

    public Mono<List<StatsPerProdTrade>> getStatsForLastNTrades() {
        // TODO make this usable for pagination
        return this.prodTradeRepository.findTop10ByOrderByStampDesc().flatMap(trade -> {
            Mono<TradeStat> devStatsMono = this.tradeStatsRepository.getDevStatsFor(trade.getSymbol(), trade.getStrategy(), trade.getTimeframe())
                    .map(this::mapToTrade);

            Mono<TradeStat> prodStatsMono = this.tradeStatsRepository.getProdStatsFor(trade.getSymbol(), trade.getStrategy(), trade.getTimeframe())
                    .map(this::mapToTrade);

            return Mono.zip(devStatsMono, prodStatsMono)
                    .map(tuple -> {
                        TradeStat devStats = tuple.getT1();
                        TradeStat prodStats = tuple.getT2();

                        // Create a new StatsPerProdTrade object with the results
                        StatsPerProdTrade result = new StatsPerProdTrade();
                        result.setId(BigDecimal.valueOf(trade.getId()));
                        result.setSymbol(SymbolEnum.fromValue(trade.getSymbol()));
                        final Set<StrategyEnum> strategies = STRATEGY_NAMES.entrySet().stream()
                                .filter(entry -> entry.getValue().equals(trade.getStrategy()))
                                .map(Map.Entry::getKey)
                                .collect(Collectors.toSet());
                        if(strategies.isEmpty()){
                            throw new IllegalArgumentException("Not StrategyEnum found for " + trade.getStrategy());
                        } else if (strategies.size() > 1){
                            throw new IllegalArgumentException("Multiple StrategyEnums found for " + trade.getStrategy());
                        }
                        result.setStrategy(strategies.stream().findFirst().get());
                        switch (trade.getTimeframe()){
                            case "15":
                                result.setTimeframe(TimeFrameEnum.M15);
                                break;
                            case "30":
                                result.setTimeframe(TimeFrameEnum.M30);
                                break;
                            case "60":
                                result.setTimeframe(TimeFrameEnum.H1);
                                break;
                        }

                        LocalDateTime stamp = trade.getStamp();
                        ZoneOffset offset = ZoneOffset.systemDefault().getRules().getOffset(stamp);
                        result.setStamp(stamp.atOffset(offset));

                        result.setProdLoses(prodStats.getLoses());
                        result.setProdWins(prodStats.getWins());
                        result.setProdTotal(prodStats.getTotal());
                        result.setProdWinPercentage(prodStats.getWinpercentage());

                        result.setDevLoses(devStats.getLoses());
                        result.setDevWins(devStats.getWins());
                        result.setDevTotal(devStats.getTotal());
                        result.setDevWinPercentage(devStats.getWinpercentage());
                        return result;
                    });
        }).collectList();
    }


    // TODO change return to Mono<>
    public Mono<List<TradeStat>> getTradeStats(final String env) {

        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> this.tradeStatsRepository.statsDevTrades(MIN_TRADES, MIN_PROFIT, WIN_PERCENTAGE)
                    .map(this::mapToTrade).collectList();
            case "PROD" -> this.tradeStatsRepository.statsProdTrades()
                    .map(this::mapToTrade).collectList();
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
    }

    public Mono<TradeStat> getStatsFor(final Signal signal, final String env) {
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" ->
                    this.tradeStatsRepository.getDevStatsFor(signal.symbol(), signal.strategy(), signal.timeframe())
                            .map(this::mapToTrade);
            case "PROD" ->
                    this.tradeStatsRepository.getProdStatsFor(signal.symbol(), signal.strategy(), signal.timeframe())
                            .map(this::mapToTrade);
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
    }

    private TradeStat mapToTrade(final TradeStatInterface entity) {
        if (entity.getSymbol() == null || entity.getSymbol().isEmpty() || entity.getStrategy() == null || entity.getStrategy().isEmpty()) {
            throw new IllegalArgumentException("Symbol or strategy is null/empty");
        }
        final TradeStat stat = new TradeStat();
        stat.setSymbol(SymbolEnum.fromValue(entity.getSymbol()));

        final Set<StrategyEnum> strategies = STRATEGY_NAMES.entrySet().stream()
                .filter(entry -> entry.getValue().equals(entity.getStrategy()))
                .map(Map.Entry::getKey)
                .collect(Collectors.toSet());
        if (strategies.isEmpty()) {
            log.warn("No StrategyEnum found for " + entity.getStrategy());
            throw new IllegalArgumentException("No StrategyEnum found for " + entity.getStrategy());
        } else if (strategies.size() > 1) {
            log.warn("Multiple StrategyEnums found for " + entity.getStrategy());
            throw new IllegalArgumentException("Multiple StrategyEnums found for " + entity.getStrategy());
        }
        stat.setStrategy(strategies.stream().findFirst().get());
        // get StrategyEnum from StrategyNameMapping using entity.getStrategy()
        if (entity.getProfit() != null) {
            stat.setProfit(BigDecimal.valueOf(entity.getProfit()).setScale(2, RoundingMode.HALF_UP));
        }
        if (entity.getLoses() != null) {
            stat.setLoses(entity.getLoses());
        }
        if (entity.getTotal() != null) {
            stat.setTotal(entity.getTotal());
        }
        if (entity.getWins() != null) {
            stat.setWins(entity.getWins());
        }
        if (entity.getWinpercentage() != null) {
            stat.setWinpercentage(BigDecimal.valueOf(entity.getWinpercentage()));
        }
        return stat;
    }


}
