package jdg.digital.forexbackend.domain.model;

import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.nio.channels.FileChannel;

@Repository
@Transactional
public interface ProdTradeRepository extends ReactiveCrudRepository<ProdTradeEntity, Integer> {

    //ProdTradeEntity findBySymbolAndStrategy(String symbol, String strategy);

    @Query(value = "SELECT COUNT(*) FROM \"ProdTrades\" WHERE symbol = :symbol AND strategy = :strategy AND openprice=0 AND activated=''")
    Mono<Integer> countActiveTrades(String symbol, String strategy);

    Flux<ProdTradeEntity> findTop10ByOrderByStampDesc();
}