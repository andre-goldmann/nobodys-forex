package jdg.digital.forexbackend.interfaces;

import jdg.digital.forexbackend.domain.*;
import jdg.digital.forexbackend.domain.model.StrategyEnum;
import jdg.digital.forexbackend.domain.model.SymbolEnum;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.List;

@RestController
@Slf4j
public class TradeController {

    @Autowired
    private TradesService tradeService;

    @Autowired
    private TradeStatsServices tradeStatsServices;

    @GetMapping("tradetats/{env}")
    public Mono<List<TradeStat>> getTradesDev(@PathVariable("env") final String env) {
        return this.tradeStatsServices.getTradeStats(env);
    }

    @GetMapping("trades/positive-profit")
    public Mono<List<Trade>> getTradesWithPositiveProfit(@RequestParam SymbolEnum symbol, @RequestParam StrategyEnum strategy) {
        return this.tradeService.getTradesWithPositiveProfit(symbol, strategy);
    }

    @GetMapping("trades/negative-profit")
    public Mono<List<Trade>> getTradesWithNegativeProfit(@RequestParam SymbolEnum symbol, @RequestParam StrategyEnum strategy) {
        return this.tradeService.getTradesWithNegativeProfit(symbol, strategy);
    }

    @GetMapping("trades/waiting/{env}")
    public Mono<List<Trade>> getWaitingTrades(@PathVariable("env") final String env) {
        return this.tradeService.getWaitingTrades(env);
    }

    @PutMapping("trades/update/{env}")
    public Mono<Trade> updateTrade(@PathVariable("env") final String env, @RequestBody Trade trade) {
        return this.tradeService.updateTrade(env, trade);
    }

    @PostMapping("signal")
    public Mono<Void> createSignal(@RequestBody Signal signal) {
        log.info("Received signal: {}", signal);
        // TODO implement signal processing
        // TODO send signal to queue
        // TODO store it in ProdDB if it is a valid signal
        return Mono.empty();
    }
}
