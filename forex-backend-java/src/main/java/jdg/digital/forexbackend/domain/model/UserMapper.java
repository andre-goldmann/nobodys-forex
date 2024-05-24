package jdg.digital.forexbackend.domain.model;

import jdg.digital.forexbackend.interfaces.users.UserDto;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface UserMapper {
    @Mapping(source = "fullName", target = "fullName")
    UserDto mapUserToDto(final UserEntity entity);

    @Mapping(source = "fullName", target = "fullName")
    UserEntity mapUserToEntity(final UserDto dto);
}
