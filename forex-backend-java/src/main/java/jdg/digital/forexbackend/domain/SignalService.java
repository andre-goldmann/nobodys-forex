package jdg.digital.forexbackend.domain;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.api_interface.AgainstTrendSignal;
import jdg.digital.api_interface.TradeStat;
import jdg.digital.forexbackend.domain.model.*;
import jdg.digital.forexbackend.interfaces.ForexProducerService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;

import java.time.DayOfWeek;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Locale;
import static jdg.digital.forexbackend.domain.TradeStatsServices.*;
import static jdg.digital.forexbackend.domain.TradeStatsServices.MIN_TRADES;

@Service
@Slf4j
@Transactional
public class SignalService {

    public static final int ACTIVE_TRADES_MAX = 4;

    @Autowired
    private SignalRepository signalRepository;

    @Autowired
    private ProdTradeRepository prodTradeRepository;

    @Autowired
    private ForexProducerService forexProducerService;

    @Autowired
    private IgnoredSignalsRepository ignoredSignalsRepository;

    @Autowired
    private AgainstTrendSignalRepository againstTrendSignalRepository;

    @Autowired
    private ObjectMapper mapper;

    @Autowired
    private TradeStatsServices tradeStatsServices;


    public Mono<AgainstTrendSignalEntity> storeAgainstTrendSignal(final AgainstTrendSignal signal){
        return this.againstTrendSignalRepository.save(AgainstTrendSignalEntity.builder()
                .symbol(signal.getSymbol())
                .timeframe(signal.getTimeframe())
                .strategy(signal.getStrategy())
                .type(signal.getType())
                .timestamp(signal.getTimestamp())
                .build());
    }

    public Mono<List<Signal>> getSignals(String env) {
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> this.signalRepository.signalsDev()
                            .map(this::entityToDto).collectList();
            case "PROD" -> this.signalRepository.signalsProd()
                            .map(this::entityToDto).collectList();
            case "FTMO" -> this.signalRepository.signalsFtmo()
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

    public Mono<String> storeSignal(Signal signal){
        return this.tradeStatsServices.getStatsFor(signal, "DEV")
                .flatMap(stats -> {

                    if (stats.getTotal() >= MIN_TRADES
                            && stats.getWinpercentage().doubleValue() < WIN_PERCENTAGE){
                        this.storeIgnoredSignal(signal, stats, "Stats not fulfilled").subscribe();
                        return Mono.just("Signal Ignored!");
                    }

                    double lots = signal.lots();
                    if (stats.getTotal() >= MIN_TRADES
                            && stats.getWinpercentage().doubleValue() >= WIN_PERCENTAGE){
                        lots = 0.1;
                    }

                    // Always store to dev
                    this.storeDevSignal(signal, lots).subscribe();

                    // Only store to ftmo if stats are fulfilled
                    if (stats.getWinpercentage().doubleValue() > FTMO_WIN_PERCENTAGE
                            && stats.getProfit().doubleValue() > FTMO_MIN_PROFIT
                            && stats.getTotal() > FTMO_MIN_TRADES) {
                        log.info("Storing ftmo signal for {}-{} with stats {}", signal.symbol(), signal.strategy(), stats);
                        this.storeFtmoSignal(signal).subscribe();
                    }

                    // Only store to prod if stats are fulfilled
                    if (stats.getWinpercentage().doubleValue() > WIN_PERCENTAGE
                            && stats.getProfit().doubleValue() > MIN_PROFIT
                            && stats.getTotal() > MIN_TRADES) {

                        return this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy())
                                .map(activeTrades -> {
                                    if (activeTrades < ACTIVE_TRADES_MAX) {
                                        log.info("Stats found for Signal of {}-{} and stats are fulfilled {}", signal.symbol(), signal.strategy(), stats);
                                        // TODO we could load prodStats here and dynamically set the lots

                                        // check if today is Thursday and if actuall time is before 16:00
                                        // if yes, then do nothing here
                                        // if no, then store the signal in prod

                                        // 1. Obtain the current date and time
                                        final LocalDateTime now = LocalDateTime.now();

                                        // 2. Check if today is Thursday
                                        final boolean isThursday = now.getDayOfWeek() == DayOfWeek.THURSDAY;

                                        // 3. Check if the current time is before 16:00
                                        final boolean isBefore16 = now.toLocalTime().isBefore(LocalTime.of(16, 0));

                                        if (isThursday && isBefore16) {
                                            log.info("Today is Thursday and the current time is before 16:00, so the signal will not be stored in prod");
                                        } else {
                                            this.storeProdSignal(signal).subscribe();
                                        }


                                        try {
                                            this.forexProducerService.sendMessage("signals", this.mapper.writeValueAsString(signal));
                                        } catch (JsonProcessingException e) {
                                            throw new RuntimeException(e);
                                        }

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

    private Mono<Boolean> storeIgnoredSignal(final Signal signal, final TradeStat stats, final String info) {

            return this.ignoredSignalsRepository.existsBySymbolAndStrategyAndTimeframe(signal.symbol(), signal.strategy(), signal.timeframe())
                    .map(exists -> {
                        if(!exists){
                            this.ignoredSignalsRepository.save(IgnoredSignalEntity.builder()
                                    .symbol(signal.symbol())
                                    .strategy(signal.strategy())
                                    .timeframe(signal.timeframe())
                                    .loses(stats.getLoses())
                                    .wins(stats.getWins())
                                    .total(stats.getTotal())
                                    .info(info)
                                    .build()).subscribe();

                            return false;
                        }
                        return exists;
                    });

            // before storing this information check if it is exists allready
            //return ignoredSignalsRepository.insert(mapper.writeValueAsString(signal), info + ": " + stats.toString());
    }

    private Mono<Void> storeDevSignal(final Signal signal, final double lots) {
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

    private Mono<Void> storeProdSignal(final Signal signal) {
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

    private Mono<Void> storeFtmoSignal(final Signal signal) {
        return this.signalRepository.insertFtmoTradeEntity(
                signal.symbol(),
                signal.timeframe(),
                signal.type(),
                signal.entry(),
                signal.sl(),
                signal.tp(),
                0.1,
                signal.strategy(),
                LocalDateTime.now());
    }

    private Mono<String> storeNewSignal(final Signal signal) {
        return this.storeDevSignal(signal, 0.01)
                .then(Mono.just("Stored new signal"));
    }
}
