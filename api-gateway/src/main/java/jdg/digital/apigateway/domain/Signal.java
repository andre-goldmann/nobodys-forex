package jdg.digital.apigateway.domain;

public record Signal(
    String symbol,
    String timestamp,
    String type,
    double entry,
    double sl,
    double tp,
    String strategy,
    boolean ignored,
    String ignoreMessage
) {}