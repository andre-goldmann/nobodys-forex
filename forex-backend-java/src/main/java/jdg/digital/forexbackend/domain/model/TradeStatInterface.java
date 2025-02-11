package jdg.digital.forexbackend.domain.model;

public interface TradeStatInterface {
    String getSymbol();
    String getStrategy();
    String getTimeframe();
    Double getProfit();
    Integer getWins();
    Integer getLoses();
    Integer getTotal();
    Double getWinpercentage();
}
