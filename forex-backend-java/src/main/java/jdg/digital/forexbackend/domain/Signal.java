package jdg.digital.forexbackend.domain;

import java.time.OffsetDateTime;

public record Signal (
    String symbol,
    OffsetDateTime timestamp,
    String type,
    double entry,
    double sl,
    double tp,
    double lots,
    String strategy,
    boolean ignored,
    String ignoreMessage
) {}