package jdg.digital.apigateway.domain;


import jdg.digital.api_interface.TradeStat;
import reactor.core.publisher.Mono;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TradeStatsService {

    @Autowired
    ForexDataServiceApi forexDataServiceApi;

    public Mono<TradeStat[]> getTradeStats(final String env) {
        return this.forexDataServiceApi.getTradeStats(env);
    }

}
