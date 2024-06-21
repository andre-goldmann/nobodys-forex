package jdg.digital.forexbackend.domain.model;

import org.springframework.data.r2dbc.repository.Modifying;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.nio.channels.FileChannel;

@Transactional
public interface TradeRepository extends ReactiveCrudRepository<TradesEntity, Integer> {

    @Query(value = "SELECT * from \"Trades\" WHERE symbol = :symbol AND strategy = :strategy AND exit > 0 ORDER BY closed DESC")
    Flux<TradesEntity> loadTrades(@Param("symbol") final String symbol, @Param("strategy") final String strategy);

    @Modifying
    @Query(value = "update \"Trades\" set exit = :exit, profit = :profit, commision = :commision, swap = :swap, closed = :closed WHERE symbol = :symbol AND id = :magic")
    Mono<Integer> updateDev(@Param("symbol") String symbol, @Param("magic") Integer magic, @Param("exit") Double exit, @Param("profit") Double profit, @Param("commision") Double commision, @Param("swap") Double swap, @Param("closed") String closed);

    @Modifying
    @Query(value = "update \"ProdTrades\" set exit = :exit, profit = :profit, commision = :commision, swap = :swap, closed = :closed WHERE symbol = :symbol AND id = :magic")
    Mono<Integer> updateProd(@Param("symbol") String symbol, @Param("magic") Integer magic, @Param("exit") Double exit, @Param("profit") Double profit, @Param("commision") Double commision, @Param("swap") Double swap, @Param("closed") String closed);

}
