package jdg.digital.forexbackend.domain.model;

import org.springframework.data.repository.reactive.ReactiveCrudRepository;

import java.util.UUID;

public interface UserEntityRepository extends ReactiveCrudRepository<UserEntity, UUID> {
}
