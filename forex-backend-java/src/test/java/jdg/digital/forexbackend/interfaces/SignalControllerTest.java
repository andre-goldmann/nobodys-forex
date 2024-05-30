package jdg.digital.forexbackend.interfaces;

import com.fasterxml.jackson.databind.ObjectMapper;
import jdg.digital.forexbackend.domain.Signal;
import jdg.digital.forexbackend.domain.TradeStatsRepository;
import jdg.digital.forexbackend.domain.model.SignalRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import java.time.OffsetDateTime;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
public class SignalControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private TradeStatsRepository tradeStatsRepository;

    @Autowired
    private SignalRepository signalRepository;

    @Test
    public void createSignalNoStatsFound() throws Exception {
        Signal signal = new Signal("EURUSD", OffsetDateTime.now(), "BUY", 1.1300, 1.1200, 1.1400, 0.01,"strategy1", false, "false");

        mockMvc.perform(post("/signals")
                        .contentType("application/json")
                        .content(objectMapper.writeValueAsString(signal)))
                .andExpect(status().isOk());

        // wenn kein Eintrag gefunden muss dieser angelegt werden
        assertEquals(1, signalRepository.count());
    }
}