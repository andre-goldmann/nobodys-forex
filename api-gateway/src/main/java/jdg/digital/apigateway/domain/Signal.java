package jdg.digital.apigateway.domain;

public record Signal(
    Integer id,
    String symbol,
    String timestamp,
    String type,
    Double entry,
    Double sl,
    Double tp,
    Double lots,
    String strategy,
    Boolean ignored,
    String ignoreMessage
) {}