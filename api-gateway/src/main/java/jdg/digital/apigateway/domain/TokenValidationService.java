package jdg.digital.apigateway.domain;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

@Service
public class TokenValidationService {
    private final String KEYCLOAK_URL = "https://172.25.128.161:8443/realms/forex_admininstrator/protocol/openid-connect/token/introspect";
    private final String CLIENT_ID = "forex_admininstrator_client";
    private final String CLIENT_SECRET = "1qFzfPvMEei1ksMIbnC9vkDyxihxtc5P";

    private RestTemplate restTemplate;

    public TokenValidationService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public boolean isValidToken(final String token) {
        final String url = KEYCLOAK_URL.replace("{realm-name}", "forex_admininstrator");

        // Create request body
        final MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
        body.add("token", token);
        body.add("client_id", CLIENT_ID);
        body.add("client_secret", CLIENT_SECRET);

        // Make request to Keycloak token validation endpoint
        final ResponseEntity<String> response = restTemplate.postForEntity(url, body, String.class);

        // Check response status
        if (response.getStatusCode() == HttpStatus.OK) {
            // Token is valid
            return true;
        } else {
            // Token is invalid
            return false;
        }
    }
}
