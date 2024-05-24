package jdg.digital.forexbackend.domain.model;

public interface TradeInterface {
    Integer getId();
    Double getProfit();
    Double getCommision();
    Double getSwap();
    Double getEntry();
    Double getExit();
}
