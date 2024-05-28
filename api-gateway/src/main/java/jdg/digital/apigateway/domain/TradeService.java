package jdg.digital.apigateway.domain;

import jdg.digital.api_interface.StrategyEnum;
import jdg.digital.api_interface.SymbolEnum;
import jdg.digital.api_interface.Trade;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.List;

@Service
public class TradeService {

    @Autowired
    ForexDataServiceApi forexDataServiceApi;

    public Mono<List<Trade>> getTradesWithPositiveProfit(final SymbolEnum symbol, final StrategyEnum strategy) {
        return this.forexDataServiceApi.getTradesWithPositiveProfit(symbol, strategy);
    }

    public Mono<List<Trade>> getTradesWithNegativeProfit(final SymbolEnum symbol, final StrategyEnum strategy) {
        return this.forexDataServiceApi.getTradesWithNegativeProfit(symbol, strategy);
    }

    public Mono<List<Signal>> getWaitingTrades(final String env) {
        return this.forexDataServiceApi.getSignals(env);
    }

    public Mono<Trade> updateTrade(final String env,Trade trade) {
        return this.forexDataServiceApi.updateTrade(env, trade);
    }
}

