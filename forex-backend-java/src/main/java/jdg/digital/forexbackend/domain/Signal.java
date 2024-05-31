package jdg.digital.forexbackend.domain;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import jdg.digital.forexbackend.utils.CustomOffsetDateTimeDeserializer;

import java.time.OffsetDateTime;

public record Signal (
    String symbol,
    @JsonDeserialize(using = CustomOffsetDateTimeDeserializer.class)
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