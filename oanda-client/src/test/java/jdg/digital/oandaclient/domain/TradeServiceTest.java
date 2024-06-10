package jdg.digital.oandaclient.domain;

import com.oanda.v20.ExecuteException;
import com.oanda.v20.RequestException;
import com.oanda.v20.account.Account;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class TradeServiceTest {

    @Autowired
    TradeService cut;

    @Autowired
    private Account accountOne;

    @BeforeEach
    void setUp() {
    }

    @Test
    void trade() throws ExecuteException, RequestException {
        this.cut.trade(accountOne, "EUR_USD", 1000, "buy");

    }
}