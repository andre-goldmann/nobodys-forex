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

    @PutMapping("trades/update/{env}")
    public Mono<Trade> updateTrade(@PathVariable("env") final String env, @RequestBody Trade trade) {
        return this.tradeService.updateTrade(env, trade);
    }

    @PostMapping("trades/updatehistory/{env}")
    public Mono<String> updatehistory(@PathVariable("env") final String env, @RequestBody TradeHistoryUpdate trade) {
        return this.tradeService.updateHistory(env, trade);
    }
}
