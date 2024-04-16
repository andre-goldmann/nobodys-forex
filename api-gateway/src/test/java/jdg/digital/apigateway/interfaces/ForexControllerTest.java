package jdg.digital.apigateway.interfaces;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockserver.springtest.MockServerTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.AutoConfigureWebTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.*;
import org.springframework.test.web.reactive.server.WebTestClient;
import org.springframework.web.client.RestTemplate;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Arrays;

import static org.springframework.security.test.web.reactive.server.SecurityMockServerConfigurers.mockJwt;
import static org.springframework.security.test.web.reactive.server.SecurityMockServerConfigurers.springSecurity;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureWebTestClient(timeout = "PT5M")
//@TiImsTestPropertySource
@MockServerTest
class ForexControllerTest {

   // private MockServerClient mockServerClient;

    @Autowired
    private WebTestClient webTestClient;

    @Autowired
    private TestRestTemplate restTemplate;
    @LocalServerPort
    int randomServerPort;
    @BeforeEach
    void setUp() {

    }

    @Test
    //@WithMockUser("Peter")
    void getSymbols() throws URISyntaxException {
        //final String baseUrl = "http://localhost:" + randomServerPort + "/api/forex/symbols";
        final String baseUrl = "http://localhost:9080/api/forex/symbols";

        URI uri = new URI(baseUrl);
        final String token = "token";
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        headers.add("X-Authorization", "Bearer " + token);
        headers.add("Content-Type", "application/json");
        ResponseEntity<String> result = this.restTemplate.exchange(uri, HttpMethod.GET, new HttpEntity<>(headers), String.class);

    }
}