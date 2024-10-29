package jdg.digital.forexbackend.domain;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.api_interface.AgainstTrendSignal;
import jdg.digital.api_interface.TradeStat;
import jdg.digital.forexbackend.domain.model.*;
import jdg.digital.forexbackend.interfaces.ForexProducerService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;

import javax.annotation.PostConstruct;
import java.math.BigDecimal;
import java.time.DayOfWeek;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.time.temporal.ChronoUnit;
import java.time.temporal.Temporal;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;

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

    @PostConstruct
    public void runOnStartup() {
        runDailyAt11PM();
    }

    private final List<String> STRATEGIES_WITH_OVER_60_PERCENT = new ArrayList<>();
    private final List<String> FTMO_STRATEGIES_WITH_OVER_60_PERCENT = new ArrayList<>();

    @Scheduled(cron = "0 0 23 * * *")
    public void runDailyAt11PM() {
        STRATEGIES_WITH_OVER_60_PERCENT.clear();
        FTMO_STRATEGIES_WITH_OVER_60_PERCENT.clear();

        this.tradeStatsServices.getTradeStats("dev", 200, 55.0).subscribe(
                stats -> {
                    stats.forEach(stat -> {
                        STRATEGIES_WITH_OVER_60_PERCENT.add(stat.getSymbol() + " " + stat.getStrategy() + " " + stat.getTimeframe());
                    });
                    log.info("############ Using strategies for DEFAULT: {}", STRATEGIES_WITH_OVER_60_PERCENT);
                },
                error -> log.error("Error while getting stats for last 10 trades", error)
        );

        this.tradeStatsServices.getTradeStats("ftmo", 200, 60.0).subscribe(
                stats -> {
                    stats.forEach(stat -> {
                        FTMO_STRATEGIES_WITH_OVER_60_PERCENT.add(stat.getSymbol() + " " + stat.getStrategy() + " " + stat.getTimeframe());
                    });
                    log.info("############ Using strategies for FTMO: {}", FTMO_STRATEGIES_WITH_OVER_60_PERCENT);
                },
                error -> log.error("Error while getting stats for last 10 trades", error)
        );
    }

    public Mono<AgainstTrendSignalEntity> storeAgainstTrendSignal(final AgainstTrendSignal signal) {
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
        return this.ignoredSignalsRepository.deleteByJson(json);
    }

    public Mono<String> storeSignal(Signal signal) {

        // check if today is Thursday and if actuall time is before 16:00
        // if yes, then do nothing here
        // if no, then store the signal in prod

        // 1. Obtain the current date and time
        final LocalDateTime now = LocalDateTime.now();

        // 2. Check if today is Thursday
        final boolean isThursday = now.getDayOfWeek() == DayOfWeek.THURSDAY
                && now.toLocalTime().isAfter(LocalTime.of(12, 30))
                && now.toLocalTime().isBefore(LocalTime.of(15, 0));

        final boolean isTuesday = now.getDayOfWeek() == DayOfWeek.TUESDAY
                && now.toLocalTime().isAfter(LocalTime.of(14, 30))
                && now.toLocalTime().isBefore(LocalTime.of(16, 30));

        final boolean isFriday = now.getDayOfWeek() == DayOfWeek.FRIDAY
                && now.toLocalTime().isAfter(LocalTime.of(14, 30))
                && now.toLocalTime().isBefore(LocalTime.of(16, 30));

        final boolean isNight = now.toLocalTime().isAfter(LocalTime.of(23, 30))
                && now.toLocalTime().isBefore(LocalTime.of(0, 4));

        if (isThursday || isTuesday || isFriday || isNight) {
            log.info("Today is Tuesday/Thursday/Friday and the current time is before "+now+", so the signal will not be stored");
            return Mono.just("Signal ignored");
        }

        // check if there is an entry within ignoredsignalsnew for this strategy
        // if so ignore this signal, otherwise check stats for this signal
        String strategy = signal.strategy();
        final Mono<Integer> filterMono;

        // when the is signal from the strategy with _DEFAULT then we need to check, if there is an entry with any strategy
        if (signal.strategy().endsWith("_DEFAULT")) {
            strategy = signal.strategy().replace("_DEFAULT", "");
            if(!STRATEGIES_WITH_OVER_60_PERCENT.contains(signal.symbol() + " " + strategy + " " + signal.timeframe())
            && !STRATEGIES_WITH_OVER_60_PERCENT.contains(signal.symbol() + " " + strategy + "_WITHOUT_REG" + " " + signal.timeframe())) {
                return Mono.just("Ignored!");
            }
            filterMono = this.ignoredSignalsRepository.countBySymbolAndStrategyLikeAndTimeframe(
                    signal.symbol(),
                    "%" + strategy + "%",
                    signal.timeframe()
            );
        } else {
            filterMono = this.ignoredSignalsRepository.countBySymbolAndStrategyAndTimeframe(
                    signal.symbol(),
                    strategy,
                    signal.timeframe()
            );
        }
        final String strategyClean = strategy;
        return filterMono.flatMap(count -> {
            if (count == 0) {
                return this.tradeStatsServices.getStatsFor(signal, "DEV")
                        .flatMap(stats -> {

                            final double winpercentage = stats.getWinpercentage().doubleValue();
                            final int total = stats.getTotal();
                            if (total >= MIN_TRADES && winpercentage < WIN_PERCENTAGE) {
                                this.storeIgnoredSignal(signal, stats, "Stats not fulfilled").subscribe();
                                return Mono.just("Signal Ignored!");
                            }

                            if (signal.strategy().endsWith("_DEFAULT")) {
                                // check if there is a strategy with loaded by
                                String strat = signal.strategy().replace("_DEFAULT", "");
                                // So this can be a strategy with "_WITHOUTH_REG" or quals to strat
                                // this strategy needs then a statistik better or equalt to prod-stats
                                //
                            }

                            double lots = signal.lots();
                            if (total >= MIN_TRADES && winpercentage >= WIN_PERCENTAGE) {
                                lots = 0.1;
                            }

                            // Always store to dev
                            this.storeDevSignal(signal, lots).subscribe();

                            // Only store to ftmo if stats are fulfilled
                            final double profit = stats.getProfit().doubleValue();
                            if (winpercentage > FTMO_WIN_PERCENTAGE && profit > FTMO_MIN_PROFIT && total > FTMO_MIN_TRADES) {
                                this.storeFtmoSignal(signal).subscribe(
                                        value -> log.info("Stored ftmo signal for {}-{} with stats {} resulted ", signal.symbol(), signal.strategy(), stats),
                                        error -> log.error("Error while Storing ftmo signal for {}-{} with stats {} resulted ", signal.symbol(), signal.strategy(), stats, error)
                                );
                            }

                            // Only store to prod if stats are fulfilled
                            if ((FTMO_STRATEGIES_WITH_OVER_60_PERCENT.contains(signal.symbol() + " " + strategyClean + " " + signal.timeframe())
                                    && FTMO_STRATEGIES_WITH_OVER_60_PERCENT.contains(signal.symbol() + " " + strategyClean + "_WITHOUT_REG" + " " + signal.timeframe()))) {

                                return this.prodTradeRepository.countActiveTrades(signal.symbol(), signal.strategy())
                                        .map(activeTrades -> {
                                            if (activeTrades < ACTIVE_TRADES_MAX) {
                                                log.info("Stats found for Signal of {}-{} and stats are fulfilled {}", signal.symbol(), signal.strategy(), stats);
                                                // TODO we could load prodStats here and dynamically set the lots

                                                this.storeProdSignal(signal).subscribe();

                                                try {
                                                    this.forexProducerService.sendMessage("signals", this.mapper.writeValueAsString(signal));
                                                } catch (JsonProcessingException e) {
                                                    log.error("Error while sending Signal to topic: ", e);
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
                                                    log.error("Error while sending Signal to topic: ", e);
                                                }

                                                return "Active trades are " + activeTrades;
                                            }
                                        });
                            } else {
                                //log.info("Stats found for Signal of {}-{} but stats are not fulfilled {}", signal.symbol(), signal.strategy(), stats);
                                return Mono.just("Stats are not fulfilled");
                            }
                        })
                        .switchIfEmpty(storeNewSignal(signal));
            }
            return Mono.just("Ignored!");
        });

    }

    private Signal ignoredSignalToDto(final IgnoredSignalInterface entity) {
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
                    if (!exists) {
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

    private Mono<Integer> storeFtmoSignal(final Signal signal) {
        return this.signalRepository.insertFtmoTradeEntity(
                signal.symbol(),
                signal.timeframe(),
                signal.type(),
                signal.entry(),
                signal.sl(),
                signal.tp(),
                1.0,
                signal.strategy(),
                LocalDateTime.now());
    }

    private Mono<String> storeNewSignal(final Signal signal) {
        return this.storeDevSignal(signal, 0.01)
                .then(Mono.just("Stored new signal"));
    }
}
