package jdg.digital.apigateway.interfaces.forex;

import jdg.digital.apigateway.domain.ForexService;
import jdg.digital.apigateway.domain.Signal;
import jdg.digital.apigateway.domain.TokenValidationService;
import jdg.digital.apigateway.domain.TradeStatsService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.reactive.server.WebTestClient;
import org.springframework.web.socket.WebSocketHandler;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(SpringExtension.class)
@WebFluxTest(controllers = ForexController.class)
class ForexControllerTest {

    @Autowired
    private WebTestClient webTestClient;

    @MockBean
    private TokenValidationService tokenValidationService;

    @MockBean
    private WebSocketHandler forexHandler;

    @MockBean
    private TradeStatsService tradeStatsService;

    @MockBean
    private ForexService forexService;

    @BeforeEach
    void setUp() {
    }

    @Test
    @WithMockUser
    void getSignals() {
        final List<Signal> signals = new ArrayList<>();
        signals.add(new Signal(1, "EURUSD", "2021-09-01T00:00:00", "BUY", 1.1234, 1.1200, 1.1300, 0.01, "strategy", false, ""));

        when(this.forexService.getSignals("env")).thenReturn(Mono.just(signals));

        this.webTestClient.get()
                .uri("/forex/signals/env")
                .exchange()
                .expectStatus().isOk()
                .expectBody(List.class)
                .value(signalsResult -> {
                    assertNotNull(signalsResult);
                    assertEquals(signals.size(), signalsResult.size());
                });
    }
}