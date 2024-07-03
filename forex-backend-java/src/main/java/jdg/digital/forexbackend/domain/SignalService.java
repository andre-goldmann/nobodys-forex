package jdg.digital.forexbackend.domain;

import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.api_interface.TradeStat;
import jdg.digital.forexbackend.domain.model.*;
import jdg.digital.forexbackend.interfaces.ForexProducerService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Locale;
;

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

    @Autowired
    private ObjectMapper mapper;

    public Mono<List<Signal>> getSignals(String env) {
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> this.signalRepository.signalsDev()
                            .map(this::entityToDto).collectList();
            case "PROD" -> this.signalRepository.signalsProd()
                            .map(this::entityToDto).collectList();
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
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

    public Mono<IgnoredSignalEntity> storeIgnoredSignal(final Signal signal, final TradeStat stats, final String info) {
        try {
            if(this.ignoredSignalsRepository.existsBySymbolStrategyAndTimeframe(signal.symbol(), signal.strategy(), signal.timeframe()).blockOptional().orElse(false)){
                return Mono.empty();
            }
            // before storing this information check if it is exists allready
            //return ignoredSignalsRepository.insert(mapper.writeValueAsString(signal), info + ": " + stats.toString());
            return this.ignoredSignalsRepository.save(IgnoredSignalEntity.builder()
                    .symbol(signal.symbol())
                    .strategy(signal.strategy())
                    .timeframe(signal.timeframe())
                    .loses(stats.getLoses())
                    .wins(stats.getWins())
                    .total(stats.getTotal())
                    .info(info)
                    .build());
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    public Mono<Void> storeDevSignal(Signal signal, double lots) {
        return this.signalRepository.insertDevTradeEntity(
                signal.symbol(),
                signal.timeframe(),
                signal.type(),
                signal.entry(),
                signal.sl(),
                signal.tp(),
                lots,
                signal.strategy(),
                LocalDateTime.now());
    }

    public Mono<Void> storeProdSignal(Signal signal) {
        return this.signalRepository.insertProdTradeEntity(
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
}
