package jdg.digital.forexbackend.domain.model;

import org.springframework.data.jpa.repository.JpaRepository;

import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;

public interface ProdTradeRepository extends JpaRepository<ProdTradeEntity, Integer> {

    ProdTradeEntity findBySymbolAndStrategy(String symbol, String strategy);

    @Modifying
    @Query(value = "INSERT INTO \"ProdTrades\" (symbol, type, entry, sl, tp, lots, strategy, stamp, activated) VALUES (:symbol, :type, :entry, :sl, :tp, :lots, :strategy, :stamp, '')", nativeQuery = true)
    void insertProdTradeEntity(@Param("symbol") String symbol, @Param("type") String type, @Param("entry") Double entry, @Param("sl") Double sl, @Param("tp") Double tp, @Param("lots") Double lots, @Param("strategy") String strategy, @Param("stamp") LocalDateTime stamp);

    @Query(value = "SELECT COUNT(*) FROM \"ProdTrades\" WHERE symbol = :symbol AND strategy = :strategy AND openprice=0 AND activated=''", nativeQuery = true)
    Integer countActiveTrades(String symbol, String strategy);
}