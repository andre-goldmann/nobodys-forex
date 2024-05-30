package jdg.digital.forexbackend.domain.model;


import org.springframework.data.r2dbc.repository.Modifying;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;

@Repository
@Transactional
public interface SignalRepository extends ReactiveCrudRepository<SignalEntity, Integer> {

    @Query(value = "SELECT * from \"Trades\" WHERE (activated IS NULL and tradeid IS NULL and openprice IS NULL) or (activated='' and tradeid = 0 and openprice = 0) limit = 5")
    Flux<SignalEntity> signalsDev();

    @Query(value = "SELECT * from \"ProdTrades\" WHERE (activated IS NULL and tradeid IS NULL and openprice IS NULL) or (activated='' and tradeid = 0 and openprice = 0)")
    Flux<SignalEntity> signalsProd();

    @Modifying
    @Query(value = "INSERT INTO \"ProdTrades\" (symbol, type, entry, sl, tp, lots, strategy, stamp, activated) VALUES (:symbol, :type, :entry, :sl, :tp, :lots, :strategy, :stamp, '')")
    Mono<Void> insertProdTradeEntity(@Param("symbol") String symbol, @Param("type") String type, @Param("entry") Double entry, @Param("sl") Double sl, @Param("tp") Double tp, @Param("lots") Double lots, @Param("strategy") String strategy, @Param("stamp") LocalDateTime stamp);

    @Modifying
    @Query(value = "INSERT INTO \"Trades\" (symbol, type, entry, sl, tp, lots, strategy, stamp, activated) VALUES (:symbol, :type, :entry, :sl, :tp, :lots, :strategy, :stamp, '')")
    Mono<Void> insertDevTradeEntity(@Param("symbol") String symbol, @Param("type") String type, @Param("entry") Double entry, @Param("sl") Double sl, @Param("tp") Double tp, @Param("lots") Double lots, @Param("strategy") String strategy, @Param("stamp") LocalDateTime stamp);
}
