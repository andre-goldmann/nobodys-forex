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

import java.time.LocalDateTime;
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

    public Mono<List<Signal>> getSignals(String env) {
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> Mono.fromCallable(
                    () -> this.signalRepository.waitingTradesDev().stream()
                            .map(this::entityToDto)
                            .toList());
            case "PROD" -> Mono.fromCallable(
                    () -> this.signalRepository.waitingTradesProd().stream()
                            .map(this::entityToDto)
                            .toList());
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
    }

    public String storeSignal(final Signal signal, final Optional<TradeStat> stats) {
        //log.info("Signal {} has stats {}", signal, stats);

        if(stats.isPresent()) {
            final Integer activeTrades = this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy());
            if (activeTrades < 4 && stats.get().getWinpercentage() > WIN_PERCENTAGE && stats.get().getProfit() > MIN_PROFIT && stats.get().getTotal() > MIN_TRADES){
                log.info("Stats found Signal of {}-{} and stats are fulfilled {}", signal.symbol(), signal.strategy(), stats.get());
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
                    log.info("Stats found Signal of {}-{} but stats are not fulfilled {}", signal.symbol(), signal.strategy(), stats.get());
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
            log.info("Stats not found Signal of {}-{}", signal.symbol(), signal.strategy());
            storeDevSignal(signal);
        }

        return "Signal processed";
    }

    private void storeDevSignal(Signal signal) {
        this.signalRepository.insertDevTradeEntity(
                signal.symbol(),
                signal.type(),
                signal.entry(),
                signal.sl(),
                signal.tp(),
                0.01,
                signal.strategy(),
                LocalDateTime.now());
    }

    public Mono<List<Signal>> getIgnoredSignals() {
        return Mono.fromCallable(
                () -> this.signalRepository.ignoredSignals().stream()
                        .map(this::ignoredSignalToDto)
                        .toList());
    }

    public Mono<Void> deleteIgnoredSignal(final String json) {
        return Mono.fromRunnable(() -> this.signalRepository.deleteByJson(json));
    }

    private Signal ignoredSignalToDto(final IgnoredSignalInterface entity)  {
            return new Signal(
                    entity.getJson(),
                    "",
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
                signalEntity.getSymbol(),
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
