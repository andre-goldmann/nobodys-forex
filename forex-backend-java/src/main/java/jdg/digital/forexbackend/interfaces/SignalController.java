package jdg.digital.forexbackend.interfaces;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.api_interface.TradeStat;
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

    public static final int ACTIVE_TRADES_MAX = 4;
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

        final Mono<TradeStat> devStatsMono = this.tradeStatsServices.getStatsFor(signal, "DEV");
        final Mono<TradeStat> prodStatsMono = this.tradeStatsServices.getStatsFor(signal, "PROD");
        final Mono<Integer> activeTradesMonot = this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy());
        return Mono.zip(devStatsMono, prodStatsMono, activeTradesMonot).map(tuple -> {

            TradeStat devStats = tuple.getT1();
            if(devStats == null){
                storeNewSignal(signal).subscribe();
                return "New Signal stored!";
            }

            if (devStats.getTotal() >= MIN_TRADES
                    && devStats.getWinpercentage().doubleValue() < WIN_PERCENTAGE){
                this.signalService.storeIgnoredSignal(signal, devStats, "Stats not fulfilled").subscribe();
                return "Signal Ignored!";
            }

            double lots = signal.lots();
            if (devStats.getTotal() >= MIN_TRADES
                    && devStats.getWinpercentage().doubleValue() >= WIN_PERCENTAGE){
                lots = 0.1;
            }

            // Always store to dev
            this.signalService.storeDevSignal(signal, lots).subscribe();
            Integer activeTradeCount = tuple.getT3();

            if (devStats.getWinpercentage().doubleValue() > WIN_PERCENTAGE
                    && devStats.getProfit().doubleValue() > TradeStatsServices.MIN_PROFIT
                    && devStats.getTotal() > MIN_TRADES
                    && activeTradeCount < ACTIVE_TRADES_MAX) {
                final TradeStat prodStats = tuple.getT2();
                if (prodStats != null && prodStats.getTotal() > MIN_TRADES
                        && prodStats.getWinpercentage().doubleValue() < WIN_PERCENTAGE) {
                    String msg = "Do not store to Prod as MinTrades have been reached but WinPercentage is " + prodStats.getWinpercentage();
                    this.signalService.storeIgnoredSignal(signal, devStats, msg).subscribe();
                    return msg;
                }

                log.info("Stats found for Signal of {}-{} and stats are fulfilled {}", signal.symbol(), signal.strategy(), devStats);
                // TODO we could load prodStats here and dynamically set the lots
                this.signalService.storeProdSignal(signal).subscribe();

                try {
                    this.forexProducerService.sendMessage("signals", this.mapper.writeValueAsString(signal));
                } catch (JsonProcessingException e) {
                    throw new RuntimeException(e);
                }
            }

            return "Signal Processed!";
        });
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
