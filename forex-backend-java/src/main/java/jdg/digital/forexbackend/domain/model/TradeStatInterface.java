package jdg.digital.forexbackend.domain.model;

public interface TradeStatInterface {
    String getSymbol();
    String getStrategy();
    double getProfit();
    int getWins();
    int getLoses();
    int getTotal();
    double getWinPercentage();
}
