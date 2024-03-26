package jdg.digital.forexbackend.interfaces.users;

import jakarta.validation.Valid;
import jdg.digital.forexbackend.domain.model.UserMapper;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import jdg.digital.forexbackend.domain.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Optional;
import java.util.UUID;

@RestController
@AllArgsConstructor
@RequestMapping(value = "/api/users")
@Slf4j
public class UserController {


    private final UserService userService;

    private final UserMapper mapper;

    @GetMapping()
    public UserDto home(){

        return UserDto
                .builder()
                .id("UUID.randomUUID()")
                .fullName("FullName")
                .email("test@gmx.de")
                .age(33)
                .build();
    }

    @GetMapping("{userId}")
    public ResponseEntity<UserDto> findUserById(@Valid @PathVariable final String userId){
        if(this.userService.findByUuid(UUID.fromString(userId)).isPresent()) {
            return ResponseEntity.ok(UserDto
                    .builder()
                    .id("UUID.randomUUID()")
                    .fullName("FullName")
                    .email("test@gmx.de")
                    .age(33)
                    .build());
        }
        return ResponseEntity.notFound().build();
    }

    @PostMapping
    public ResponseEntity<UserDto> addUser(@Valid @RequestBody final UserDto userRequestDto){
        log.info("Storing:");
        log.info("Request {}", userRequestDto.toString());
        final Optional<UserDto> user = this.userService.findByUuid(UUID.fromString(userRequestDto.id));
        if(user.isPresent()) {
            return ResponseEntity.ok(user.get());
        }
        final UserDto dto = this.userService.save(userRequestDto);
        return ResponseEntity.ok(dto);
    }
}
