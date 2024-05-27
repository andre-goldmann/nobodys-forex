package jdg.digital.forexbackend.domain.model;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface TradeRepository extends JpaRepository<TradesEntity, Integer> {

    @Query(value = "SELECT * from \"Trades\" WHERE symbol = :symbol AND strategy = :strategy AND exit > 0 ORDER BY closed DESC", nativeQuery = true)
    List<TradesEntity> loadTrades(@Param("symbol") final String symbol, @Param("strategy") final String strategy);

    @Query(value = "SELECT * from \"Trades\" WHERE activated='' and tradeid=0 and openprice=0", nativeQuery = true)
    List<TradesEntity> waitingTradesDev();

    @Query(value = "SELECT * from \"ProdTrades\" WHERE (activated IS NULL and tradeid IS NULL and openprice IS NULL) or (activated='' and tradeid = 0 and openprice = 0)", nativeQuery = true)
    List<TradesEntity> waitingTradesProd();

    //@Query(value = "SELECT COUNT(*) FROM \"Trades\" WHERE symbol = :symbol AND strategy = :strategy AND exit > 0", nativeQuery = true)
    //Long countTrades(@Param("symbol") String symbol, @Param("strategy") String strategy);
}
