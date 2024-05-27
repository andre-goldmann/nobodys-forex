package jdg.digital.forexbackend.domain;

import jdg.digital.forexbackend.domain.model.ProdTradeEntity;
import jdg.digital.forexbackend.domain.model.ProdTradeRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("test")
class TradesServiceIT {

    @Autowired
    private TradesService tradesService;

    @Autowired
    private ProdTradeRepository prodTradeRepository;

    @BeforeEach
    void setUp() {
    }

    @Test
    void checkSignal() {
        // Arrange
        Signal signal = new Signal("symbol", "timestamp", "type", 1.23, 0, 0, "strategy", true, "");
        TradeStat stats = new TradeStat();

        // Act
        tradesService.storeSignal(signal, stats);

        // Assert
        /*ProdTradeEntity prodTradeEntity = prodTradeRepository.findBySymbolAndStrategy(signal.symbol(), signal.strategy());
        assertNotNull(prodTradeEntity);
        assertEquals(signal.symbol(), prodTradeEntity.getSymbol());
        assertEquals(signal.strategy(), prodTradeEntity.getStrategy());
    */
    }
}