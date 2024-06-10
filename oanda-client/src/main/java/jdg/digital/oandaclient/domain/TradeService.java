package jdg.digital.oandaclient.domain;

import com.oanda.v20.Context;
import com.oanda.v20.ExecuteException;
import com.oanda.v20.RequestException;
import com.oanda.v20.account.Account;
import com.oanda.v20.account.AccountID;
import com.oanda.v20.order.MarketOrderRequest;
import com.oanda.v20.order.OrderCreateRequest;
import com.oanda.v20.order.OrderCreateResponse;
import com.oanda.v20.primitives.Instrument;
import com.oanda.v20.trade.TradeSetClientExtensionsRequest;
import com.oanda.v20.trade.TradeSetDependentOrdersRequest;
import com.oanda.v20.trade.TradeSpecifier;
import com.oanda.v20.transaction.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@Slf4j
public class TradeService {

    @Autowired
    private Context oandaCtx;

    // das sollte eigentlich das Signal bekommen und dann die Order erstellen
    // am Ende muss dann noch die Info an den Server übertragen werden
    public void trade(
            final Account account,
            final String instrument,
            final int units,
            final String side) throws ExecuteException, RequestException {

        AccountID accountId = account.getId();
        final List<Instrument> instruments = oandaCtx.account.instruments(accountId).getInstruments();
        instruments.forEach(i -> log.info("Instrument: {}", i.getName()));
        final Instrument tradeableInstrument = instruments.stream()
                .filter(i -> i.getName().toString().equals(instrument))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Instrument not found"));
        log.info("Setup trade for {}", tradeableInstrument);

        /*final OrderCreateResponse resp = oandaCtx.order.create(new OrderCreateRequest(accountId)
                .setOrder(new MarketOrderRequest()
                        .setInstrument(tradeableInstrument.getName())
                        .setUnits(10)
                )
        );
        TransactionID orderTransId;
        TransactionID tradeTransId;

        Transaction orderTrans = resp.getOrderCreateTransaction();
        if (orderTrans.getType() != TransactionType.MARKET_ORDER)
            throw new IllegalArgumentException("Created order type "+ orderTrans.getType() + " != MARKET");
        orderTransId = resp.getOrderCreateTransaction().getId();
        tradeTransId = resp.getOrderFillTransaction().getId();

        System.out.println("TEST - PUT /accounts/{accountID}/trades/{tradeSpecifier}/clientExtensions");
        System.out.println("CHECK 200 - The Trade's Client Extensions have been updated as requested, expecting tag and comment to match what was set.");

        TradeClientExtensionsModifyTransaction trans = oandaCtx.trade.setClientExtensions(
                new TradeSetClientExtensionsRequest(accountId, new TradeSpecifier(tradeTransId))
                        .setClientExtensions(new ClientExtensions()
                                .setComment("this is a good trade")
                                .setTag("good")
                        )
        ).getTradeClientExtensionsModifyTransaction();
        if (!trans.getTradeClientExtensionsModify().getTag().toString().equals("good"))
            throw new IllegalStateException("Tag "+trans.getTradeClientExtensionsModify().getTag()+" != good");

        System.out.println("TEST - PUT /accounts/{accountID}/trades/{tradeSpecifier}/orders");
        System.out.println("CHECK 200 - The Trade's dependent Orders have been modified as requested, expecting pending TP with matching tradeId");

        TakeProfitOrderTransaction tp = oandaCtx.trade.setDependentOrders(
                new TradeSetDependentOrdersRequest(accountId, new TradeSpecifier(tradeTransId))
                        .setTakeProfit(new TakeProfitDetails().setPrice(2.0))
                        .setStopLoss(new StopLossDetails().setPrice(1.0))
        ).getTakeProfitOrderTransaction();
        if (!tp.getTradeID().equals(tradeTransId))
            throw new IllegalArgumentException("Dependent tradeId "+tp.getTradeID()+" != "+tradeTransId);*/


    }
}
