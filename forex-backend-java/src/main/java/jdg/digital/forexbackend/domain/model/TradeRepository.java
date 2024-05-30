package jdg.digital.forexbackend.domain.model;

import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Flux;

@Transactional
public interface TradeRepository extends ReactiveCrudRepository<TradesEntity, Integer> {

    @Query(value = "SELECT * from \"Trades\" WHERE symbol = :symbol AND strategy = :strategy AND exit > 0 ORDER BY closed DESC")
    Flux<TradesEntity> loadTrades(@Param("symbol") final String symbol, @Param("strategy") final String strategy);



    //@Query(value = "SELECT COUNT(*) FROM \"Trades\" WHERE symbol = :symbol AND strategy = :strategy AND exit > 0", nativeQuery = true)
    //Long countTrades(@Param("symbol") String symbol, @Param("strategy") String strategy);
}
