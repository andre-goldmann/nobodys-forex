package jdg.digital.forexbackend.domain;

public record Signal (
        String symbol,
        String timestamp,
        String type,
        double entry,
        double sl,
        double tp,
        String strategy
) {}