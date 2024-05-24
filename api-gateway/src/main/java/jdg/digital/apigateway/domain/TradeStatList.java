package jdg.digital.apigateway.domain;

import jdg.digital.api_interface.TradeStat;
import lombok.Builder;

import java.util.List;

@Builder
public class TradeStatList {
    private List<TradeStat> stats;
}
