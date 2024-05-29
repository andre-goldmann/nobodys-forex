package jdg.digital.forexbackend.interfaces;

import jdg.digital.forexbackend.domain.Signal;
import jdg.digital.forexbackend.domain.SignalService;
import jdg.digital.forexbackend.domain.TradeStatsServices;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Optional;

@RestController
@Slf4j
@RequestMapping("signals")
public class SignalController {

    @Autowired
    private SignalService signalService;

    @Autowired
    private TradeStatsServices tradeStatsServices;

    @GetMapping("/{env}")
    public Mono<List<Signal>> getSignals(@PathVariable("env") final String env) {
        return this.signalService.getSignals(env);
    }

    @GetMapping("/ignored")
    public Mono<List<Signal>> getIgnoredSignals() {
        return this.signalService.getIgnoredSignals();
    }

    @DeleteMapping("/ignored/delete")
    public Mono<Void> deleteIgnoredSignal(@RequestParam String json) {
        return this.signalService.deleteIgnoredSignal(json);
    }

    @PostMapping
    public Mono<String> createSignal(@RequestBody Signal signal) {
        return this.tradeStatsServices.getStatsFor(signal)
                .flatMap(stats -> {
                    if (stats != null) {
                        return Mono.just(this.signalService.storeSignal(signal, Optional.of(stats)));
                    } else {
                        return Mono.just("Trade not created");
                    }
                });
    }

}
