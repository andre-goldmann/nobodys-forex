package jdg.digital.forexbackend.domain;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.forexbackend.domain.model.IgnoredSignalInterface;
import jdg.digital.forexbackend.domain.model.ProdTradeRepository;
import jdg.digital.forexbackend.domain.model.SignalEntity;
import jdg.digital.forexbackend.domain.model.SignalRepository;
import jdg.digital.forexbackend.interfaces.ForexProducerService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Locale;

@Service
@Slf4j
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

    @Transactional
    public String storeSignal(final Signal signal, final TradeStat stats) {
        log.info("Signal {} has stats {}", signal, stats);

        final Integer activeTrades = this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy());
        if(activeTrades < 4) {
            this.prodTradeRepository.insertProdTradeEntity(
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

                final Signal newSignal = new Signal(
                        signal.symbol(),
                        signal.timestamp(),
                        signal.type(),
                        signal.entry(),
                        signal.sl(),
                        signal.tp(),
                        signal.strategy(),
                        true,
                        "Ignore because there more then " + activeTrades + " active trade.");
                this.forexProducerService.sendMessage("signals", new ObjectMapper().writeValueAsString(newSignal));
            } catch (JsonProcessingException e) {
                log.error("Error sending signal to queue", e);
                throw new RuntimeException(e);
            }
        }

        return "Signal processed";
    }

    public Mono<List<Signal>> getIgnoredSignals() {
        return Mono.fromCallable(
                () -> this.signalRepository.ignoredSignals().stream()
                        .map(this::ignoredSignalToDto)
                        .toList());
    }

    private Signal ignoredSignalToDto(final IgnoredSignalInterface entity)  {

            return new Signal(
                    entity.getJson(),
                    "",
                    "",
                    0.0,
                    0.0,
                    0.0,
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
                signalEntity.getStrategy(),
                false,
                "");
    }

}
