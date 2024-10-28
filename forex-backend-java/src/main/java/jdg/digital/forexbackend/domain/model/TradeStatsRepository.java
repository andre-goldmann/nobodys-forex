package jdg.digital.forexbackend.domain.model;

import jdg.digital.api_interface.Trade;
import jdg.digital.forexbackend.domain.model.TradeStatEntity;
import jdg.digital.forexbackend.domain.model.TradeStatInterface;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.nio.channels.FileChannel;

@Repository
@Transactional
public interface TradeStatsRepository extends ReactiveCrudRepository<TradeStatEntity, Integer> {

    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       timeframe,\n" +
            "       sum(profit - \"Trades\".swap - \"Trades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            " FROM  \"Trades\"\n" +
            //"WHERE activated!='' AND openprice > 0 and exit > 0\n" +
            " WHERE ((activated IS NOT NULL or activated!='') and exit > 0 and openprice > 0)" +
            " GROUP BY symbol, strategy, timeframe\n" +
            " HAVING\n" +
            "    count(*) > :minTrades\n" +
            "   AND sum(profit - \"Trades\".swap - \"Trades\".commision) > :minProfit\n" +
            "   AND COUNT(CASE WHEN profit > 0 THEN 1 END) > COUNT(CASE WHEN profit < 0 THEN 1 END)\n" +
            "   AND ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) > :winPercentage\n" +
            " ORDER BY symbol, sum(profit) DESC")
    Flux<TradeStatInterface> statsDevTrades(@Param("minTrades") Integer minTrades, @Param("minProfit") Double minProfit, @Param("winPercentage") Double winPercentage);

    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       timeframe,\n" +
            "       sum(profit - \"ProdTrades\".swap - \"ProdTrades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            " FROM  \"ProdTrades\"\n" +
            //"WHERE activated!='' AND openprice > 0 --and exit > 0\n" +
            " WHERE ((activated IS NOT NULL or activated!='') and openprice > 0 and exit > 0)" +
            " GROUP BY symbol, strategy, timeframe\n" +
            " HAVING\n" +
            "    --count(*) > 150\n" +
            "   sum(profit - \"ProdTrades\".swap - \"ProdTrades\".commision) > 5\n" +
            "   AND COUNT(CASE WHEN profit > 0 THEN 1 END) > COUNT(CASE WHEN profit < 0 THEN 1 END)\n" +
            "   --AND ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) > 55\n" +
            " ORDER BY symbol, sum(profit) DESC")
    Flux<TradeStatInterface> statsProdTrades();

    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       timeframe,\n" +
            "       sum(profit - \"FtmoTrades\".swap - \"FtmoTrades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            " FROM  \"FtmoTrades\"\n" +
            //"WHERE activated!='' AND openprice > 0 --and exit > 0\n" +
            " WHERE ((activated IS NOT NULL or activated!='') and openprice > 0 and exit > 0)" +
            " GROUP BY symbol, strategy, timeframe\n" +
            " HAVING\n" +
            "    --count(*) > 150\n" +
            "   sum(profit - \"FtmoTrades\".swap - \"FtmoTrades\".commision) > 5\n" +
            "   AND COUNT(CASE WHEN profit > 0 THEN 1 END) > COUNT(CASE WHEN profit < 0 THEN 1 END)\n" +
            "   --AND ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) > 55\n" +
            " ORDER BY symbol, sum(profit) DESC")
    Flux<TradeStatInterface> statsFtmoTrades();

    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       timeframe,\n" +
            "       sum(profit - \"Trades\".swap - \"Trades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            " FROM  \"Trades\"\n" +
            " WHERE ((activated IS NOT NULL or activated!='') and exit > 0 and openprice > 0)" +
            " and symbol = :symbol and strategy = :strategy and timeframe = :timeframe\n " +
            " GROUP BY symbol, strategy, timeframe\n"
    )
    Mono<TradeStatInterface> getDevStatsFor(@Param("symbol") String symbol, @Param("strategy") String strategy, @Param("timeframe") String timeframe);


    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       timeframe,\n" +
            "       sum(profit - \"ProdTrades\".swap - \"ProdTrades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            " FROM  \"ProdTrades\"\n" +
            " WHERE ((activated IS NOT NULL or activated!='') and exit > 0 and openprice > 0)" +
            " and symbol = :symbol and strategy = :strategy and timeframe = :timeframe\n " +
            " GROUP BY symbol, strategy, timeframe\n"
    )
    Mono<TradeStatInterface> getProdStatsFor(@Param("symbol") String symbol, @Param("strategy") String strategy, @Param("timeframe") String timeframe);

    @Query(value = "SELECT symbol,\n" +
            "       strategy,\n" +
            "       timeframe,\n" +
            "       sum(profit - \"FtmoTrades\".swap - \"FtmoTrades\".commision) as profit,\n" +
            "       --sum(swap) as swap,\n" +
            "       --sum(commision) as commision,\n" +
            "       COUNT(CASE WHEN profit > 0 THEN 1 END) AS wins,\n" +
            "       COUNT(CASE WHEN profit < 0 THEN 1 END) AS loses,\n" +
            "       count(*) as total,\n" +
            "       ROUND((COUNT(CASE WHEN profit > 0 THEN 1 END) * 100.0) / COUNT(*), 2) AS winpercentage\n" +
            " FROM  \"FtmoTrades\"\n" +
            " WHERE ((activated IS NOT NULL or activated!='') and exit > 0 and openprice > 0)" +
            " and symbol = :symbol and strategy = :strategy and timeframe = :timeframe\n" +
            " GROUP BY symbol, strategy, timeframe\n"
    )
    Mono<TradeStatInterface> getFtmoStatsFor(@Param("symbol") String symbol, @Param("strategy") String strategy, @Param("timeframe") String timeframe);
}
