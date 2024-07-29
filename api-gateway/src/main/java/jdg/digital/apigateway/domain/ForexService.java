package jdg.digital.apigateway.domain;

import jdg.digital.api_interface.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.List;

@Service
public class ForexService {

    @Autowired
    ForexDataServiceApi forexDataServiceApi;

    public Mono<List<Trade>> getTradesWithPositiveProfit(final SymbolEnum symbol, final StrategyEnum strategy) {
        return this.forexDataServiceApi.getTradesWithPositiveProfit(symbol, strategy);
    }

    public Mono<List<Trade>> getTradesWithNegativeProfit(final SymbolEnum symbol, final StrategyEnum strategy) {
        return this.forexDataServiceApi.getTradesWithNegativeProfit(symbol, strategy);
    }

    public Mono<List<Signal>> getSignals(final String env) {
        return this.forexDataServiceApi.getSignals(env);
    }

    public Mono<List<Signal>> getIgnoredSignals() {
        return this.forexDataServiceApi.getIgnoredSignals();
    }

    public Mono<Trade> updateTrade(final String env,Trade trade) {
        return this.forexDataServiceApi.updateTrade(env, trade);
    }

    public Mono<Void> deleteIgnoredSignal(final String json) {
        return this.forexDataServiceApi.deleteIgnoredSignal(json);
    }

    public Mono<String> updateHistory(String env, TradeHistoryUpdate tradeHistoryUpdate) {
        return this.forexDataServiceApi.updateHistory(env, tradeHistoryUpdate);
    }

    public Mono<List<StatsPerProdTrade>> getStatsForLastNTrades() {
        return this.forexDataServiceApi.getStatsForLastNTrades();
    }

    public Mono<List<Trade>> getTrades(final String env) {
        return this.forexDataServiceApi.getTrades(env);
    }

    public Mono<List<Trade>> searchTradesById(final String env, Integer tradeId) {
        return this.forexDataServiceApi.searchTradesById(env, tradeId);
    }
}

