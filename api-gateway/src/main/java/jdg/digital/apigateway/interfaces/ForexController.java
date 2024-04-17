package jdg.digital.apigateway.interfaces;

import jakarta.servlet.http.HttpServletRequest;
import jdg.digital.apigateway.domain.TokenValidationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.jwt.Jwt;

import java.util.List;

@RestController
@RequestMapping("forex")
@Slf4j
public class ForexController {

    @Autowired
    private TokenValidationService tokenValidationService;

    @GetMapping("/symbols")
    public ResponseEntity<List<String>> getSymbols(Authentication authentication, HttpServletRequest request){

        final String authorization = request.getHeader("authorization");
        if(authorization == null || authorization.isEmpty()){
            return ResponseEntity.badRequest().build();
        }
        final StringBuilder headersBuilder = new StringBuilder();
        // Get all header names and print them
        request.getHeaderNames().asIterator().forEachRemaining(headerName -> {
            headersBuilder.append(headerName).append(": ").append(request.getHeader(headerName)).append("\n");
        });
        log.info(headersBuilder.toString());

        /*log.info(request.getHeader("origin"));
        log.info(request.getHeader("authorization").replace("Bearer ", ""));
        log.info(request.getHeader("content-type"));
        log.info(request.getHeader("accept"));*/
        // Same exception as Spring throws, this happens because there seem to be issues with the
        // keystore beeing used
        //log.info("is valid: {}",this.tokenValidationService.isValidToken(request.getHeader("authorization").replace("Bearer ", "")));
        return ResponseEntity.ok(List.of("USDCAD", "EURUSD", "GBPUSD", "JPYUSD"));
        // actually not working
        /*if (authentication != null && authentication.getPrincipal() instanceof Jwt) {
            final Jwt jwt = (Jwt) authentication.getPrincipal();
            final String token = jwt.getTokenValue();
            if(this.tokenValidationService.isValidToken(token)) {
                // Now you have the bearer token
                //return ResponseEntity.badRequest().build();
                return ResponseEntity.ok(List.of("USDCAD", "EURUSD", "GBPUSD", "JPYUSD"));
            }
            log.error("Authenticated but token is invalid!!!");
            return ResponseEntity.badRequest().build();

        } else {
            // No bearer token found
            //No bearer token found
            if(authentication != null && authentication.getPrincipal() != null) {
                log.error("Not authenticated: {}", authentication.getPrincipal());
            }else {
                log.error("Not authenticated: {}", authentication);
            }
            return ResponseEntity.badRequest().build();
        }*/
    }
}
