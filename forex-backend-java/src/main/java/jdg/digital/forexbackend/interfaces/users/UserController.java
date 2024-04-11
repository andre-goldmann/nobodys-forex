package jdg.digital.forexbackend.interfaces.users;

import jakarta.validation.Valid;
import jdg.digital.forexbackend.domain.model.UserMapper;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import jdg.digital.forexbackend.domain.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@AllArgsConstructor
@RequestMapping(value = "/api/users")
@Slf4j
public class UserController {

    private final UserService userService;

    private final UserMapper mapper;

    @GetMapping()
    public ResponseEntity<List<UserDto>> all(JwtAuthenticationToken principal){

        if(!authentificated(principal)){
            return ResponseEntity.status(401).build();
        }

        return ResponseEntity.ok(Collections.singletonList(UserDto
                .builder()
                .id("UUID.randomUUID()")
                .fullName("FullName")
                .email("test@gmx.de")
                .age(33)
                .build()));
    }

    @GetMapping("{userId}")
    public ResponseEntity<UserDto> findUserById(JwtAuthenticationToken principal,
                                                @Valid @PathVariable final String userId){

        if(!authentificated(principal)){
            return ResponseEntity.status(401).build();
        }

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
    public ResponseEntity<UserDto> addUser(JwtAuthenticationToken principal,
                                           @Valid @RequestBody final UserDto userRequestDto){
        if(!authentificated(principal)){
            return ResponseEntity.status(401).build();
        }
        log.info("Storing:");
        log.info("Request {}", userRequestDto.toString());
        final Optional<UserDto> user = this.userService.findByUuid(UUID.fromString(userRequestDto.id));
        if(user.isPresent()) {
            return ResponseEntity.ok(user.get());
        }
        final UserDto dto = this.userService.save(userRequestDto);
        return ResponseEntity.ok(dto);
    }

    private boolean authentificated(final JwtAuthenticationToken principal) {
        log.info("Checking if principal is authenticate: {}", principal);
        final Collection<String> authorities = principal.getAuthorities()
                .stream()
                .map(GrantedAuthority::getAuthority)
                .toList();
        log.info("authorities: {}", authorities);
        return authorities.isEmpty();
    }
}
