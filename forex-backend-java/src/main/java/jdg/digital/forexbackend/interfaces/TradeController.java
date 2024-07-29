package jdg.digital.forexbackend.interfaces;

import jdg.digital.api_interface.*;
import jdg.digital.forexbackend.domain.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.List;

@RestController
@Slf4j
@RequestMapping("trades")
public class TradeController {

    @Autowired
    private TradesService tradeService;

    @Autowired
    private TradeStatsServices tradeStatsServices;

    @GetMapping("/{env}")
    public Mono<List<Trade>> getTrades(@PathVariable("env") final String env) {
        return this.tradeService.getTrades(env);
    }

    @GetMapping("/byid/{env}/{tradeId}")
    public Mono<List<Trade>> searchTradesById(@PathVariable("env") final String env, @PathVariable("tradeId") final Integer tradeId) {
        return this.tradeService.searchTrades(env, tradeId);
    }

    @GetMapping("tradetats/{env}")
    public Mono<List<TradeStat>> getTradesDev(@PathVariable("env") final String env) {
        return this.tradeStatsServices.getTradeStats(env);
    }

    @GetMapping("statsforlastntrades")
    public Mono<List<StatsPerProdTrade>> getStatsForLastNTrades() {
        return this.tradeStatsServices.getStatsForLastNTrades();
    }

    @GetMapping("positive-profit")
    public Mono<List<Trade>> getTradesWithPositiveProfit(@RequestParam SymbolEnum symbol, @RequestParam StrategyEnum strategy) {
        return this.tradeService.getTradesWithPositiveProfit(symbol, strategy);
    }

    @GetMapping("negative-profit")
    public Mono<List<Trade>> getTradesWithNegativeProfit(@RequestParam SymbolEnum symbol, @RequestParam StrategyEnum strategy) {
        return this.tradeService.getTradesWithNegativeProfit(symbol, strategy);
    }

    @PutMapping("update/{env}")
    public Mono<Trade> updateTrade(@PathVariable("env") final String env, @RequestBody Trade trade) {
        return this.tradeService.updateTrade(env, trade);
    }

    @PostMapping("updatehistory/{env}")
    public Mono<String> updatehistory(@PathVariable("env") final String env, @RequestBody TradeHistoryUpdate trade) {
        return this.tradeService.updateHistory(env, trade);
    }
}
