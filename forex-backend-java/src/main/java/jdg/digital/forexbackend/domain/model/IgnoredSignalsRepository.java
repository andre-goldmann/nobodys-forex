package jdg.digital.forexbackend.domain.model;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

@Transactional
public interface IgnoredSignalsRepository extends JpaRepository<IgnoredSignalEntity, Integer>{

    @Modifying
    @Query(value = "INSERT INTO \"IgnoredSignals\" (json, reason) VALUES (:json, :reason)", nativeQuery = true)
    void insert(@Param("json") String json, @Param("reason") String reason);
}
