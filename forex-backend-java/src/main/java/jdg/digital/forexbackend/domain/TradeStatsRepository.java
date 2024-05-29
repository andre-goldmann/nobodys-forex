package jdg.digital.forexbackend.domain;

import jdg.digital.forexbackend.domain.model.TradesEntity;
import jdg.digital.forexbackend.domain.model.TradeStatInterface;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface TradeStatsRepository extends JpaRepository<TradesEntity, Integer> {

    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       sum(profit - \"Trades\".swap - \"Trades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            "FROM  \"Trades\"\n" +
            //"WHERE activated!='' AND openprice > 0 and exit > 0\n" +
            "WHERE ((activated IS NOT NULL or activated!='') and exit > 0 and openprice > 0)" +
            "GROUP BY symbol, strategy\n" +
            "HAVING\n" +
            "    count(*) > ?1\n" +
            "   AND sum(profit - \"Trades\".swap - \"Trades\".commision) > ?2\n" +
            "   AND COUNT(CASE WHEN profit > 0 THEN 1 END) > COUNT(CASE WHEN profit < 0 THEN 1 END)\n" +
            "   AND ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) > ?3\n" +
            "ORDER BY symbol, sum(profit) DESC", nativeQuery = true)
    List<TradeStatInterface> statsDevTrades(Integer minTrades, Double minProfit, Double winPercentage);

    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       sum(profit - \"ProdTrades\".swap - \"ProdTrades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            "FROM  \"ProdTrades\"\n" +
            //"WHERE activated!='' AND openprice > 0 --and exit > 0\n" +
            "WHERE ((activated IS NOT NULL or activated!='') and openprice > 0)" +
            "GROUP BY symbol, strategy\n" +
            "HAVING\n" +
            "    --count(*) > 150\n" +
            "   sum(profit - \"ProdTrades\".swap - \"ProdTrades\".commision) > 5\n" +
            "   AND COUNT(CASE WHEN profit > 0 THEN 1 END) > COUNT(CASE WHEN profit < 0 THEN 1 END)\n" +
            "   --AND ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) > 55\n" +
            "ORDER BY symbol, sum(profit) DESC", nativeQuery = true)
    List<TradeStatInterface> statsProdTrades();

    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       sum(profit - \"Trades\".swap - \"Trades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            "FROM  \"Trades\"\n" +
            //"WHERE activated!='' AND openprice > 0 and exit > 0\n" +
            "WHERE ((activated IS NOT NULL or activated!='') and exit > 0 and openprice > 0)" +
            " and symbol = ?1 and strategy = ?2\n " +
            "GROUP BY symbol, strategy\n" +
            //"HAVING\n" +
            //"    count(*) > ?3\n" +
            //"   AND sum(profit - \"Trades\".swap - \"Trades\".commision) > ?4\n" +
            //"   AND COUNT(CASE WHEN profit > 0 THEN 1 END) > COUNT(CASE WHEN profit < 0 THEN 1 END)\n" +
            //"   AND ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) > ?5\n" +
            "ORDER BY symbol, sum(profit) DESC", nativeQuery = true)
    TradeStatInterface getStatsFor(String symbol, String strategy);
}
