package jdg.digital.forexbackend.domain.model;


import org.springframework.data.r2dbc.repository.Modifying;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
@Transactional
public interface IgnoredSignalsRepository extends ReactiveCrudRepository<IgnoredSignalEntity, Integer> {

    @Modifying
    @Query(value = "INSERT INTO \"IgnoredSignals\" (json, reason) VALUES (:json, :reason)")
    Mono<Void> insert(@Param("json") String json, @Param("reason") String reason);

    @Query(value = "SELECT json, count(*) from \"IgnoredSignals\" group by json")
    Flux<IgnoredSignalInterface> ignoredSignals();

    @Modifying
    @Query(value = "delete from \"IgnoredSignals\" where json = :json")
    Mono<Void> deleteByJson(@Param("json") String json);

    Mono<Boolean> existsBySymbolAndStrategyAndTimeframe(String symbol, String strategy, String timeframe);
}
