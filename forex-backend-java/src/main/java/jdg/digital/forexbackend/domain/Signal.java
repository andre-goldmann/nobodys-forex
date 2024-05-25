package jdg.digital.forexbackend.domain;

import com.fasterxml.jackson.annotation.JsonProperty;

public record Signal (
        String symbol,
        String timestamp,
        String type,
        String entry,
        int sl,
        int tp,
        String strategy
) {}