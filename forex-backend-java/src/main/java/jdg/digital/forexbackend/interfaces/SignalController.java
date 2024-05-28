package jdg.digital.forexbackend.interfaces;

import jdg.digital.forexbackend.domain.Signal;
import jdg.digital.forexbackend.domain.SignalService;
import jdg.digital.forexbackend.domain.TradeStatsServices;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.List;

@RestController
@Slf4j
@RequestMapping("signals")
public class SignalController {

    @Autowired
    private SignalService signalService;

    @Autowired
    private TradeStatsServices tradeStatsServices;

    @GetMapping("/{env}")
    public Mono<List<Signal>> getWaitingTrades(@PathVariable("env") final String env) {
        return this.signalService.getSignals(env);
    }

    @PostMapping
    public Mono<String> createSignal(@RequestBody Signal signal) {
        log.info("Signal: {}", signal);
        return this.tradeStatsServices.getStatsFor(signal.symbol(), signal.strategy())
                .map(stats -> {
                    log.info("Stats: {}", stats);
                    if (stats != null) {
                        return this.signalService.storeSignal(signal, stats);
                    } else {
                        return "Trade not created";
                    }
                });
    }

}
