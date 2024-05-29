package jdg.digital.forexbackend.domain.model;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Transactional
public interface TradeRepository extends JpaRepository<TradesEntity, Integer> {

    @Query(value = "SELECT * from \"Trades\" WHERE symbol = :symbol AND strategy = :strategy AND exit > 0 ORDER BY closed DESC", nativeQuery = true)
    List<TradesEntity> loadTrades(@Param("symbol") final String symbol, @Param("strategy") final String strategy);



    //@Query(value = "SELECT COUNT(*) FROM \"Trades\" WHERE symbol = :symbol AND strategy = :strategy AND exit > 0", nativeQuery = true)
    //Long countTrades(@Param("symbol") String symbol, @Param("strategy") String strategy);
}
