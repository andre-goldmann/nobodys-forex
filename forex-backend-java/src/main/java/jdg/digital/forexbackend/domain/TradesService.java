package jdg.digital.forexbackend.domain;

import jdg.digital.api_interface.*;
import jdg.digital.forexbackend.domain.model.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

import static jdg.digital.forexbackend.domain.model.StrategyNameMapping.STRATEGY_NAMES;

@Service
@Slf4j
@Transactional
public class TradesService {

    @Autowired
    private TradeRepository tradeRepository;

    public Mono<List<Trade>> getTradesWithPositiveProfit(final SymbolEnum symbolEnum, final StrategyEnum strategyEnum) {
        log.info("Search for {}-{}", symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum));
        return this.tradeRepository.loadTrades(symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum))
                .map(this::entityToDto).collectList();
    }

    public Mono<List<Trade>> getTradesWithNegativeProfit(final SymbolEnum symbolEnum, final StrategyEnum strategyEnum) {
        log.info("Search for {}-{}", symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum));
        return this.tradeRepository.loadTrades(symbolEnum.getValue(), STRATEGY_NAMES.get(strategyEnum))
                .map(this::entityToDto).collectList();
    }

    public Mono<String> updateTrade(final String env, final TradeUpdateDto tradeUpdateDto) {
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> this.tradeRepository.updateTrade(
                            tradeUpdateDto.getSymbol().getValue().replace("#", "").replace(".r", ""),
                            tradeUpdateDto.getMagic(),
                            tradeUpdateDto.getProfit().doubleValue(),
                            tradeUpdateDto.getSwap().doubleValue(),
                            tradeUpdateDto.getCommision().doubleValue(),
                            tradeUpdateDto.getClosed()
                    )
                    .map(result -> {
                        if (result == 1) {
                            return "Trade updated";
                        } else {
                            return "Trade not updated";
                        }
                    });
            case "PROD" -> this.tradeRepository.updateProdTrade(
                            tradeUpdateDto.getSymbol().getValue().replace("#", "").replace(".r", ""),
                            tradeUpdateDto.getMagic(),
                            tradeUpdateDto.getProfit().doubleValue(),
                            tradeUpdateDto.getSwap().doubleValue(),
                            tradeUpdateDto.getCommision().doubleValue(),
                            tradeUpdateDto.getClosed()
                    )
                    .map(result -> {
                        if (result == 1) {
                            return "Trade updated";
                        } else {
                            return "Trade not updated";
                        }
                    });
            case "FTMO" -> this.tradeRepository.updateFtmoTrade(
                            tradeUpdateDto.getSymbol().getValue().replace("#", "").replace(".r", ""),
                            tradeUpdateDto.getMagic(),
                            tradeUpdateDto.getProfit().doubleValue(),
                            tradeUpdateDto.getSwap().doubleValue(),
                            tradeUpdateDto.getCommision().doubleValue(),
                            tradeUpdateDto.getClosed()
                    )
                    .map(result -> {
                        if (result == 1) {
                            return "Trade updated";
                        } else {
                            return "Trade not updated";
                        }
                    });
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
    }

    public Mono<String> activateTrade(final String env, final TradeActivationDto tradeActivationDto){
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> this.tradeRepository.activateTrade(
                            tradeActivationDto.getSymbol().getValue().replace("#", "").replace(".r", ""),
                            tradeActivationDto.getMagic(),
                            tradeActivationDto.getTimestamp(),
                            tradeActivationDto.getOpenPrice().doubleValue())
                    .map(result -> {
                        if (result == 1) {
                            return "Trade updated";
                        } else {
                            return "Trade not updated";
                        }
                    });
            case "PROD" -> this.tradeRepository.activateProdTrade(
                            tradeActivationDto.getSymbol().getValue().replace("#", "").replace(".r", ""),
                            tradeActivationDto.getMagic(),
                            tradeActivationDto.getTimestamp(),
                            tradeActivationDto.getOpenPrice().doubleValue())
                    .map(result -> {
                        if (result == 1) {
                            return "Trade updated";
                        } else {
                            return "Trade not updated";
                        }
                    });
            case "FTMO" -> this.tradeRepository.activateFtmoTrade(
                            tradeActivationDto.getSymbol().getValue().replace("#", "").replace(".r", ""),
                            tradeActivationDto.getMagic(),
                            tradeActivationDto.getTimestamp(),
                            tradeActivationDto.getOpenPrice().doubleValue())
                    .map(result -> {
                        if (result == 1) {
                            return "Trade updated";
                        } else {
                            return "Trade not updated";
                        }
                    });
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
    }

    /*
    def activateSignalProd(tradeActivationDto:SignalActivationDto):
    #print("Activating Trade", tradeActivationDto)
    with Session.begin() as session:
        storeSignal = session.query(ProdSignal).filter(ProdSignal.symbol == tradeActivationDto.symbol, ProdSignal.id == tradeActivationDto.magic).first()
        if storeSignal is not None:
            storeSignal.activated=tradeActivationDto.timestamp
            storeSignal.openprice=tradeActivationDto.open_price
            session.commit()
            session.close()
        else:
            print("No Trade found for ", tradeActivationDto)
     */


    public Mono<String> updateHistory(final String env, final TradeHistoryUpdate update) {
        /*if(update.getMagic() != null) {
            if (224497 == update.getMagic()
                    || 225290 == update.getMagic()
                    || 225291 == update.getMagic()
                    || 225292 == update.getMagic()
                    || 224455 == update.getMagic()) {
                log.info("############## updatehistory: {}", update);
            }
        }*/

        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> this.tradeRepository.updateDev(
                            update.getSymbol().getValue().replace("#", "").replace(".r", ""),
                            update.getMagic(),
                            update.getExit().doubleValue(),
                            update.getProfit().doubleValue(),
                            update.getCommision().doubleValue(),
                            update.getSwap().doubleValue(),
                            update.getClosed())
                    .map(result -> {
                        if (result == 1) {
                            return "Tradehistory updated";
                        } else {
                            return "Tradehistory not updated";
                        }
                    })
                    .doOnError(error -> log.error("Error updating trade: {}", error.getMessage()));
            case "PROD" -> this.tradeRepository.updateProd(
                            update.getSymbol().getValue(),
                            update.getMagic(),
                            update.getExit().doubleValue(),
                            update.getProfit().doubleValue(),
                            update.getCommision().doubleValue(),
                            update.getSwap().doubleValue(),
                            update.getClosed())
                    .map(result -> {
                        if (result == 1) {
                            return "Tradehistory updated";
                        } else {
                            return "Tradehistory not updated";
                        }
                    })
                    .doOnError(error -> log.error("Error updating trade: {}", error.getMessage()));
            case "FTMO" -> this.tradeRepository.updateFtmo(
                            update.getSymbol().getValue(),
                            update.getMagic(),
                            update.getExit().doubleValue(),
                            update.getProfit().doubleValue(),
                            update.getCommision().doubleValue(),
                            update.getSwap().doubleValue(),
                            update.getClosed())
                    .doOnError(error -> log.error("Error updating trade: {}", error.getMessage()))
                    .map(result -> {
                        if (result == 1) {
                            return "Tradehistory updated";
                        } else {
                            return "Tradehistory not updated";
                        }
                    });
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };

    }

    public Mono<List<Trade>> getTrades(String env) {
        return switch (env.toUpperCase(Locale.getDefault())) {
            case "DEV" -> this.tradeRepository.getDevTrades()
                    .map(this::entityToDto).collectList();
            case "PROD" -> this.tradeRepository.getProdTrades()
                    .map(this::entityToDto).collectList();
            case "FTMO" -> this.tradeRepository.getFtmoTrades()
                    .map(this::entityToDto).collectList();
            default -> throw new IllegalArgumentException("Undefined env " + env);
        };
    }

    public Mono<List<Trade>> searchTrades(final String env, final Integer tradeId) {
        // load from Prod
        return this.tradeRepository.findByIdWithinProd(tradeId)
                .log()
                .flatMap(
                        // Search within dev
                        entity -> this.tradeRepository.findBySymbolAndStrategyAndTypeAndSlAndTp(
                                        entity.getSymbol(),
                                        entity.getStrategy(),
                                        entity.getType(),
                                        entity.getSl(),
                                        entity.getTp())
                                .map(this::entityToDto)
                                .collectList()
                );
    }


    private Trade entityToDto(final TradesEntity entity) {
        final Trade trade = new Trade();
        trade.setId(entity.getId());
        trade.setSymbol(SymbolEnum.fromValue(entity.getSymbol()));
        final Set<StrategyEnum> strategies = STRATEGY_NAMES.entrySet().stream()
                .filter(entry -> entry.getValue().equals(entity.getStrategy()))
                .map(Map.Entry::getKey)
                .collect(Collectors.toSet());
        if (strategies.isEmpty()) {
            throw new IllegalArgumentException("Not StrategyEnum found for " + entity.getStrategy());
        } else if (strategies.size() > 1) {
            throw new IllegalArgumentException("Multiple StrategyEnums found for " + entity.getStrategy());
        }
        trade.setStrategy(strategies.stream().findFirst().get());
        if (entity.getOpenprice() != null) {
            trade.setOpenprice(BigDecimal.valueOf(entity.getOpenprice()));
        }

        if (entity.getExit() != null) {
            trade.setExit(BigDecimal.valueOf(entity.getExit()));
        }
        trade.setEntry(BigDecimal.valueOf(entity.getEntry()));
        if (entity.getProfit() != null && entity.getCommision() != null && entity.getSwap() != null) {
            final BigDecimal profit = BigDecimal.valueOf(entity.getProfit() - entity.getCommision() - entity.getSwap());
            trade.setProfit(profit.setScale(2, RoundingMode.HALF_UP));
        }

        if (entity.getClosed() != null && !entity.getClosed().isEmpty()) {
            final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy.MM.dd HH:mm");
            final LocalDateTime localDateTime = LocalDateTime.parse(entity.getClosed(), formatter);
            trade.setClosed(localDateTime.atOffset(ZoneOffset.UTC));
        }
        if (entity.getActivated() != null && !entity.getActivated().isEmpty()) {
            final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy.MM.dd HH:mm:ss");
            final LocalDateTime localDateTime = LocalDateTime.parse(entity.getActivated(), formatter);
            trade.setActivated(localDateTime.atOffset(ZoneOffset.UTC));
        }
        if (entity.getProfit() != null) {
            trade.setProfit(BigDecimal.valueOf(entity.getProfit()));
        }
        switch (entity.getTimeframe().toUpperCase()) {
            case "M1" -> trade.setTimeframe(TimeFrameEnum.M1);
            case "M5" -> trade.setTimeframe(TimeFrameEnum.M5);
            case "15" -> trade.setTimeframe(TimeFrameEnum.M15);
            case "30" -> trade.setTimeframe(TimeFrameEnum.M30);
            case "60" -> trade.setTimeframe(TimeFrameEnum.H1);
            case "240" -> trade.setTimeframe(TimeFrameEnum.H4);
            case "D1" -> trade.setTimeframe(TimeFrameEnum.D1);
            case "W1" -> trade.setTimeframe(TimeFrameEnum.W1);
            case "MN1" -> trade.setTimeframe(TimeFrameEnum.MN1);
            default -> throw new IllegalArgumentException("Undefined timeframe " + entity.getTimeframe());
        }
        //trade.setTimeframe(TimeFrameEnum.fromValue(entity.getTimeframe()));
        trade.setType(TradeTypeEnum.valueOf(entity.getType().toUpperCase()));
        return trade;
    }

}
