package jdg.digital.forexbackend.interfaces;

import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.api_interface.AgainstTrendSignal;
import jdg.digital.forexbackend.domain.Signal;
import jdg.digital.forexbackend.domain.SignalService;
import jdg.digital.forexbackend.domain.model.AgainstTrendSignalEntity;
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
    private ObjectMapper mapper;

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

    @PostMapping("/againsttrendsignal")
    public Mono<AgainstTrendSignalEntity> createSignal(@RequestBody AgainstTrendSignal signal) {
        log.info("Received against trend signal: {}", signal);
        return this.signalService.storeAgainstTrendSignal(signal);
    }

    @PostMapping
    public Mono<String> createSignal(@RequestBody Signal signal) {
        return this.signalService.storeSignal(signal);
    }

}
