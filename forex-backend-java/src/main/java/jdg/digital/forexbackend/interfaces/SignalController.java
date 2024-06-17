package jdg.digital.forexbackend.interfaces;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.forexbackend.domain.Signal;
import jdg.digital.forexbackend.domain.SignalService;
import jdg.digital.forexbackend.domain.TradeStatsServices;
import jdg.digital.forexbackend.domain.model.ProdTradeRepository;
import jdg.digital.forexbackend.domain.model.SignalRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.List;

import static jdg.digital.forexbackend.domain.TradeStatsServices.MIN_TRADES;
import static jdg.digital.forexbackend.domain.TradeStatsServices.WIN_PERCENTAGE;

@RestController
@Slf4j
@RequestMapping("signals")
public class SignalController {

    @Autowired
    private SignalService signalService;

    @Autowired
    private TradeStatsServices tradeStatsServices;

    @Autowired
    private SignalRepository signalRepository;

    @Autowired
    private ProdTradeRepository prodTradeRepository;

    @Autowired
    private ForexProducerService forexProducerService;


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

    @PostMapping
    public Mono<String> createSignal(@RequestBody Signal signal) {

        return this.tradeStatsServices.getStatsFor(signal, "DEV")
                .flatMap(stats -> {

                    if (stats.getTotal() >= MIN_TRADES
                            && stats.getWinpercentage() < WIN_PERCENTAGE){
                        this.signalService.storeIgnoredSignal(signal, stats,"Stats not fulfilled").subscribe();
                        return Mono.just("Signal Ignored!");
                    }

                    double lots = signal.lots();
                    if (stats.getTotal() >= MIN_TRADES
                            && stats.getWinpercentage() >= WIN_PERCENTAGE){
                        lots = 0.1;
                    }

                    // Always store to dev
                    this.signalService.storeDevSignal(signal, lots).subscribe();

                    // Only store to prod if stats are fulfilled
                    if (stats.getWinpercentage() > WIN_PERCENTAGE
                            && stats.getProfit() > TradeStatsServices.MIN_PROFIT
                            && stats.getTotal() > MIN_TRADES) {

                        return this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy())
                                .map(activeTrades -> {
                                    if (activeTrades < 4) {
                                        log.info("Stats found for Signal of {}-{} and stats are fulfilled {}", signal.symbol(), signal.strategy(), stats);
                                        //  load prodStats here (and dynamically set the lots or) ignore the signal
                                        // generated start
                                        this.tradeStatsServices.getStatsFor(signal, "PROD").flatMap(prodStats -> {
                                            if (prodStats.getTotal() >= MIN_TRADES
                                                    && prodStats.getWinpercentage() < WIN_PERCENTAGE){
                                                return Mono.just(true);
                                            } else {
                                                return Mono.just(false);
                                            }
                                        }).subscribe(ignored -> {
                                            if (ignored){
                                                log.info("Stats found for Signal of {}-{} but prod-stats have reached total trades {}", signal.symbol(), signal.strategy(), stats);
                                                return;
                                            }
                                            final Signal newSignal = new Signal(
                                                    1,
                                                    signal.symbol(),
                                                    signal.timeframe(),
                                                    signal.timestamp(),
                                                    signal.type(),
                                                    signal.entry(),
                                                    signal.sl(),
                                                    signal.tp(),
                                                    0.01,
                                                    signal.strategy(),
                                                    true,
                                                    "Signal stored in prod");

                                            // Store to prod (only if stats are fulfilled)
                                            this.signalService.storeProdSignal(newSignal).subscribe();

                                            try {
                                                this.forexProducerService.sendMessage("signals", this.mapper.writeValueAsString(newSignal));
                                            } catch (JsonProcessingException e) {
                                                throw new RuntimeException(e);
                                            }
                                        });
                                        // generated end
                                        /*this.signalService.storeProdSignal(signal).subscribe();

                                        try {
                                            this.forexProducerService.sendMessage("signals", this.mapper.writeValueAsString(signal));
                                        } catch (JsonProcessingException e) {
                                            throw new RuntimeException(e);
                                        }*/

                                        return "Signal also stored in prod!";
                                    } else {
                                        log.info("Stats found for Signal of {}-{} but amount of active trades ({}) allready reached", signal.symbol(), signal.strategy(), activeTrades);

                                        final Signal newSignal = new Signal(
                                               1,
                                                signal.symbol(),
                                                signal.timeframe(),
                                                signal.timestamp(),
                                                signal.type(),
                                                signal.entry(),
                                                signal.sl(),
                                                signal.tp(),
                                                signal.lots(),
                                                signal.strategy(),
                                                true,
                                                "Ignore because there more then " + activeTrades + " active trade.");

                                        try {
                                            this.forexProducerService.sendMessage("signals", this.mapper.writeValueAsString(newSignal));
                                        } catch (JsonProcessingException e) {
                                            throw new RuntimeException(e);
                                        }

                                        return "Active trades are " + activeTrades;
                                    }
                                });
                    } else {
                        log.info("Stats found for Signal of {}-{} but stats are not fulfilled {}", signal.symbol(), signal.strategy(), stats);
                        return Mono.just("Stats are not fulfilled");
                    }
                })

                .switchIfEmpty(storeNewSignal(signal));
    }

    private Mono<String> storeNewSignal(final Signal signal) {
        return this.signalRepository.insertDevTradeEntity(
                        signal.symbol(),
                        signal.timeframe(),
                        signal.type(),
                        signal.entry(),
                        signal.sl(),
                        signal.tp(),
                        signal.lots(),
                        signal.strategy(),
                        LocalDateTime.now())
                .then(Mono.just("Stored new signal"));
    }

}
