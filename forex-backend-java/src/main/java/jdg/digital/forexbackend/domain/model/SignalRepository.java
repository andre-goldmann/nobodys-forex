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

    @Query(value = "SELECT * from \"Trades\" WHERE (activated IS NULL and openprice IS NULL) or (activated='' and openprice = 0) or (activated='' and openprice IS NULL) order by stamp desc limit 20")
    Flux<SignalEntity> signalsDev();

    @Query(value = "SELECT * from \"ProdTrades\" WHERE (activated IS NULL and openprice IS NULL) or (activated='' and openprice = 0) or (activated='' and openprice IS NULL) order by stamp desc")
    Flux<SignalEntity> signalsProd();

    @Query(value = "SELECT * from \"FtmoTrades\" WHERE (activated IS NULL and openprice IS NULL) or (activated='' and openprice = 0) or (activated='' and openprice IS NULL) order by stamp desc")
    Flux<SignalEntity> signalsFtmo();

    @Modifying
    @Query(value = "INSERT INTO \"ProdTrades\" (symbol, timeframe, type, entry, sl, tp, lots, strategy, stamp, activated) VALUES (:symbol, :timeframe, :type, :entry, :sl, :tp, :lots, :strategy, :stamp, '')")
    Mono<Void> insertProdTradeEntity(@Param("symbol") String symbol, @Param("timeframe") String timeframe, @Param("type") String type, @Param("entry") Double entry, @Param("sl") Double sl, @Param("tp") Double tp, @Param("lots") Double lots, @Param("strategy") String strategy, @Param("stamp") LocalDateTime stamp);

    @Modifying
    @Query(value = "INSERT INTO \"Trades\" (symbol, timeframe, type, entry, sl, tp, lots, strategy, stamp, activated) VALUES (:symbol, :timeframe, :type, :entry, :sl, :tp, :lots, :strategy, :stamp, '')")
    Mono<Void> insertDevTradeEntity(@Param("symbol") String symbol, @Param("timeframe") String timeframe, @Param("type") String type, @Param("entry") Double entry, @Param("sl") Double sl, @Param("tp") Double tp, @Param("lots") Double lots, @Param("strategy") String strategy, @Param("stamp") LocalDateTime stamp);

    @Modifying
    @Query(value = "INSERT INTO \"FtmoTrades\" (symbol, timeframe, type, entry, sl, tp, lots, strategy, stamp, activated) VALUES (:symbol, :timeframe, :type, :entry, :sl, :tp, :lots, :strategy, :stamp, '')")
    Mono<Integer> insertFtmoTradeEntity(@Param("symbol") String symbol, @Param("timeframe") String timeframe, @Param("type") String type, @Param("entry") Double entry, @Param("sl") Double sl, @Param("tp") Double tp, @Param("lots") Double lots, @Param("strategy") String strategy, @Param("stamp") LocalDateTime stamp);
}
