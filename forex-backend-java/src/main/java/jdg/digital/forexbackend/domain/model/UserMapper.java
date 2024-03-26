package jdg.digital.forexbackend.model;

import org.goldmann.backend.interfaces.users.UserDto;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface UserMapper {
    @Mapping(source = "fullName", target = "fullName")
    UserDto mapUserToDto(final UserEntity entity);

    @Mapping(source = "fullName", target = "fullName")
    UserEntity mapUserToEntity(final UserDto dto);
}
