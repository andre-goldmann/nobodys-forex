package jdg.digital.apigateway.domain;

import jdg.digital.api_interface.StrategyEnum;
import jdg.digital.api_interface.SymbolEnum;
import jdg.digital.api_interface.Trade;
import jdg.digital.api_interface.TradeStat;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.List;

@Service
public class ForexDataServiceApi {
    private WebClient webClient;

    public ForexDataServiceApi(final WebClient.Builder webClientBuilder,
                               @Value("${forex.data.service.url}") final String forexDataServiceUrl) {
        this.webClient = webClientBuilder
                //.filter(new ServerBearerExchangeFilterFunction())
                .baseUrl(forexDataServiceUrl)
                .build();
    }

    public Mono<TradeStat[]> getTradeStats(final String env) {
        return this.webClient
                .get()
                .uri(uriBuilder -> uriBuilder.path("/tradetats/{env}").build(env))
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .bodyToMono(TradeStat[].class);
                //.log();
    }

    public Mono<List<Trade>> getTradesWithPositiveProfit(final SymbolEnum symbol, final StrategyEnum strategy) {
        return this.webClient
                .get()
                .uri(uriBuilder -> uriBuilder
                        .path("/trades/positive-profit")
                        .queryParam("symbol", symbol)
                        .queryParam("strategy", strategy)
                        .build())
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference<List<Trade>>() {
                });
    }

    public Mono<List<Trade>> getTradesWithNegativeProfit(final SymbolEnum symbol, final StrategyEnum strategy) {
        return this.webClient
                .get()
                .uri(uriBuilder -> uriBuilder
                        .path("/trades/negative-profit")
                        .queryParam("symbol", symbol)
                        .queryParam("strategy", strategy)
                        .build())
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference<List<Trade>>() {
                });
    }

    public Mono<List<Trade>> getWaitingTrades(final String env) {
        return this.webClient
                .get()
                .uri(uriBuilder -> uriBuilder.path("/trades/waiting/{env}").build(env))
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference<List<Trade>>() {
                });
    }

    public Mono<Trade> updateTrade(final String env, final Trade trade) {
        return this.webClient
                .put()
                .uri(uriBuilder -> uriBuilder.path("/trades/update/{env}").build(env))
                .accept(MediaType.APPLICATION_JSON)
                .body(Mono.just(trade), Trade.class)
                .retrieve()
                .bodyToMono(Trade.class);
    }
}