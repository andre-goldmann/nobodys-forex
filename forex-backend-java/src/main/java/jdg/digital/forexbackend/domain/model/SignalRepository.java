package jdg.digital.forexbackend.domain.model;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Transactional
public interface SignalRepository extends JpaRepository<SignalEntity, Integer> {

    @Query(value = "SELECT * from \"Trades\" WHERE activated='' and tradeid=0 and openprice=0", nativeQuery = true)
    List<SignalEntity> waitingTradesDev();

    @Query(value = "SELECT * from \"ProdTrades\" WHERE (activated IS NULL and tradeid IS NULL and openprice IS NULL) or (activated='' and tradeid = 0 and openprice = 0)", nativeQuery = true)
    List<SignalEntity> waitingTradesProd();

    @Query(value = "SELECT json, count(*) from \"IgnoredSignals\" group by json", nativeQuery = true)
    List<IgnoredSignalInterface> ignoredSignals();

    @Modifying
    @Query(value = "delete from \"IgnoredSignals\" where json = ?1", nativeQuery = true)
    void deleteByJson(final String json);
}
