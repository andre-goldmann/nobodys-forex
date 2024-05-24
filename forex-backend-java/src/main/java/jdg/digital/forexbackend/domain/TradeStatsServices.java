package jdg.digital.forexbackend.domain;

import jdg.digital.forexbackend.domain.model.StrategyEnum;
import jdg.digital.forexbackend.domain.model.SymbolEnum;
import jdg.digital.forexbackend.domain.model.TradeStatInterface;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import static jdg.digital.forexbackend.domain.model.StrategyNameMapping.STRATEGY_NAMES;

@Service
@Slf4j
public class TradeStatsServices {

    @Autowired
    private TradeStatsRepository tradeStatsRepository;

    // TODO change return to Mono<>
    public Mono<List<TradeStat>> getTradeStats(final String env) {
        switch (env.toUpperCase()){
            case "DEV": return Mono.fromCallable(
                    () -> this.tradeStatsRepository.statsDevTrades()
                            .stream()
                            .map(e -> mapToTrade(e))
                            .toList()
            );
            case "PROD": return Mono.fromCallable(
                    () -> this.tradeStatsRepository.statsProdTrades()
                            .stream()
                            .map(e -> mapToTrade(e))
                            .toList()
            );
            default: throw new IllegalArgumentException("Undefined env " + env);
        }
    }

    private TradeStat mapToTrade(final TradeStatInterface entity) {
        if(entity.getSymbol() == null || entity.getSymbol().isEmpty() || entity.getStrategy() == null || entity.getStrategy().isEmpty()){
            throw new IllegalArgumentException("Symbol or strategy is null/empty");
        }
        final TradeStat stat = new TradeStat();
        stat.setSymbol(SymbolEnum.fromValue(entity.getSymbol()));
        /*stat.setStrategy(StrategyEnum.fromValue(
                    entity.getStrategy()
                            .replace("-", "_")
                            .replace(" ", "_")
                            .toUpperCase()
                )
        );*/
        final Set<StrategyEnum> strategies = STRATEGY_NAMES.entrySet().stream()
                .filter(entry -> entry.getValue().equals(entity.getStrategy()))
                .map(Map.Entry::getKey)
                .collect(Collectors.toSet());
        if(strategies.size() == 0){
            throw new IllegalArgumentException("Not StrategyEnum found for " + entity.getStrategy());
        } else if (strategies.size() > 1){
            throw new IllegalArgumentException("Multiple StrategyEnums found for " + entity.getStrategy());

        }
        stat.setStrategy(strategies.stream().findFirst().get());
        // get StrategyEnum from StrategyNameMapping using entity.getStrategy()

        stat.setProfit(BigDecimal.valueOf(entity.getProfit()).setScale(2, RoundingMode.HALF_UP).doubleValue());
        stat.setLoses(entity.getLoses());
        stat.setLoses(entity.getLoses());
        stat.setWins(entity.getWins());
        stat.setWinpercentage(entity.getWinPercentage());
        return stat;
    }

}
