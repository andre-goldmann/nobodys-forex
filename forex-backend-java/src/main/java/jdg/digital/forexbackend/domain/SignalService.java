package jdg.digital.forexbackend.domain;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.forexbackend.domain.model.*;
import jdg.digital.forexbackend.interfaces.ForexProducerService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;import java.time.OffsetDateTime;
import java.util.List;
import java.util.Locale;
import java.util.Optional;

import static jdg.digital.forexbackend.domain.TradeStatsServices.*;

@Service
@Slf4j
@Transactional
public class SignalService {

    @Autowired
    private SignalRepository signalRepository;

    @Autowired
    private ProdTradeRepository prodTradeRepository;

    @Autowired
    private ForexProducerService forexProducerService;

    @Autowired
    private IgnoredSignalsRepository ignoredSignalsRepository;

    public Mono<List<Signal>> getSignals(String env) {
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> this.signalRepository.signalsDev()
                            .map(this::entityToDto).collectList();
            case "PROD" -> this.signalRepository.signalsProd()
                            .map(this::entityToDto).collectList();
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
    }

    public Mono<String> storeSignal(final Signal signal, final Optional<TradeStat> stats) {
        //log.info("Signal {} has stats {}", signal, stats);

        if(stats.isPresent() && stats.get().getWinpercentage() > WIN_PERCENTAGE && stats.get().getProfit() > MIN_PROFIT && stats.get().getTotal() > MIN_TRADES) {
            return this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy()).map(activeTrades -> {
                if (activeTrades < 4) {
                    log.info("Stats found for Signal of {}-{} and stats are fulfilled {}", signal.symbol(), signal.strategy(), stats.get());
                    storeDevSignal(signal);

                    this.signalRepository.insertProdTradeEntity(
                            signal.symbol(),
                            signal.timeframe(),
                            signal.type(),
                            signal.entry(),
                            signal.sl(),
                            signal.tp(),
                            0.01,
                            signal.strategy(),
                            LocalDateTime.now()).flatMap(signalEntity -> {
                                log.info("Signal {} inserted in prod", signalEntity);
                                return Mono.just("Signal processed");
                            });
                    try {
                        this.forexProducerService.sendMessage("signals", new ObjectMapper().writeValueAsString(signal));
                    } catch (JsonProcessingException e) {
                        log.error("Error sending signal to queue", e);
                        throw new RuntimeException(e);
                    }
                } else {
                    log.info("Stats found for Signal of {}-{} but stats are not fulfilled {}", signal.symbol(), signal.strategy(), stats.get());
                    storeDevSignal(signal);

                    final Signal newSignal = new Signal(
                            signal.id(),
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
                        this.forexProducerService.sendMessage("signals", new ObjectMapper().writeValueAsString(newSignal));
                    } catch (JsonProcessingException e) {
                        log.error("Error sending signal to queue", e);
                        throw new RuntimeException(e);
                    }
                }
                return "Signal processed";
            });
        }

        /*if(stats.isPresent()) {
            final Integer activeTrades = this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy());
            if (activeTrades < 4 && stats.get().getWinpercentage() > WIN_PERCENTAGE && stats.get().getProfit() > MIN_PROFIT && stats.get().getTotal() > MIN_TRADES){
                log.info("Stats found for Signal of {}-{} and stats are fulfilled {}", signal.symbol(), signal.strategy(), stats.get());
                storeDevSignal(signal);

                this.signalRepository.insertProdTradeEntity(
                        signal.symbol(),
                        signal.type(),
                        signal.entry(),
                        signal.sl(),
                        signal.tp(),
                        0.01,
                        signal.strategy(),
                        LocalDateTime.now());
                try {
                    this.forexProducerService.sendMessage("signals", new ObjectMapper().writeValueAsString(signal));
                } catch (JsonProcessingException e) {
                    log.error("Error sending signal to queue", e);
                    throw new RuntimeException(e);
                }
            } else {
                try {

                    if (stats.get().getTotal() >= MIN_TRADES && stats.get().getWinpercentage() <= WIN_PERCENTAGE) {
                        this.ignoredSignalsRepository.insert(signal.symbol() + "-" + signal.strategy(),
                             "Ignored, because it has "+stats.get().getLoses()+" failed Trades (All: "+stats.get().getTotal()+", Sucess: "+stats.get().getWins()+") and Win-Percentage is "+stats.get().getWinpercentage()+"!");
                    }

                    log.info("Stats found for Signal of {}-{} but stats are not fulfilled {}", signal.symbol(), signal.strategy(), stats.get());
                    storeDevSignal(signal);

                    final Signal newSignal = new Signal(
                            signal.symbol(),
                            signal.timestamp(),
                            signal.type(),
                            signal.entry(),
                            signal.sl(),
                            signal.tp(),
                            signal.lots(),
                            signal.strategy(),
                            true,
                            "Ignore because there more then " + activeTrades + " active trade.");
                    this.forexProducerService.sendMessage("signals", new ObjectMapper().writeValueAsString(newSignal));
                } catch (JsonProcessingException e) {
                    log.error("Error sending signal to queue", e);
                    throw new RuntimeException(e);
                }
            }
        } else {
            log.info("Stats not found for Signal of {}-{}", signal.symbol(), signal.strategy());
            storeDevSignal(signal);
        }*/

        return Mono.just("Signal processed");
    }

    private void storeDevSignal(Signal signal) {
        this.signalRepository.insertDevTradeEntity(
                signal.symbol(),
                signal.timeframe(),
                signal.type(),
                signal.entry(),
                signal.sl(),
                signal.tp(),
                0.01,
                signal.strategy(),
                LocalDateTime.now());
    }

    public Mono<List<Signal>> getIgnoredSignals() {
        return this.ignoredSignalsRepository.ignoredSignals()
                        .map(this::ignoredSignalToDto).collectList();
    }

    public Mono<Void> deleteIgnoredSignal(final String json) {
        return Mono.fromRunnable(() -> this.ignoredSignalsRepository.deleteByJson(json));
    }

    private Signal ignoredSignalToDto(final IgnoredSignalInterface entity)  {
        return new Signal(
                0,
                entity.getJson(),
                "",
                OffsetDateTime.now(),
                "",
                0.0,
                0.0,
                0.0,
                0.01,
                "",
                true,
                "");
    }

    private Signal entityToDto(final SignalEntity signalEntity) {
        return new Signal(
                signalEntity.getId(),
                signalEntity.getSymbol(),
                signalEntity.getTimeframe(),
                signalEntity.getStamp(),
                signalEntity.getType(),
                signalEntity.getEntry(),
                signalEntity.getSl(),
                signalEntity.getTp(),
                signalEntity.getLots(),
                signalEntity.getStrategy(),
                false,
                "");
    }

}
