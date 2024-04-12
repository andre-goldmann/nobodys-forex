package jdg.digital.apigateway.interfaces;

import jdg.digital.apigateway.domain.TokenValidationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.jwt.Jwt;

import java.util.List;

@RestController
@RequestMapping("forex")
@Slf4j
@CrossOrigin(origins = "https://192.168.2.183")
public class ForexController {

    @Autowired
    private TokenValidationService tokenValidationService;

    @GetMapping("/symbols")
    public ResponseEntity<List<String>> getSymbols(Authentication authentication){
        if (authentication != null && authentication.getPrincipal() instanceof Jwt) {
            final Jwt jwt = (Jwt) authentication.getPrincipal();
            final String token = jwt.getTokenValue();
            if(this.tokenValidationService.isValidToken(token)) {
                // Now you have the bearer token
                //return ResponseEntity.badRequest().build();
                return ResponseEntity.ok(List.of("USDCAD", "EURUSD", "GBPUSD", "JPYUSD"));
            }
            return ResponseEntity.badRequest().build();

        } else {
            // No bearer token found
            //No bearer token found
            return ResponseEntity.badRequest().build();
        }

    }
}
