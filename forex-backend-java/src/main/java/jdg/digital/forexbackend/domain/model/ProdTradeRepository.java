package jdg.digital.forexbackend.domain.model;

import org.springframework.data.jpa.repository.JpaRepository;

import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;

public interface ProdTradeRepository extends JpaRepository<ProdTradeEntity, Integer> {

    ProdTradeEntity findBySymbolAndStrategy(String symbol, String strategy);

    @Query(value = "SELECT COUNT(*) FROM \"ProdTrades\" WHERE symbol = :symbol AND strategy = :strategy AND openprice=0 AND activated=''", nativeQuery = true)
    Integer countActiveTrades(String symbol, String strategy);

}