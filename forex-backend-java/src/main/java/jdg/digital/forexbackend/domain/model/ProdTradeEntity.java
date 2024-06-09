package jdg.digital.forexbackend.domain.model;


import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

import java.time.LocalDateTime;

@Table(name = "\"ProdTrades\"")
@Getter
@Setter
@ToString
@Accessors(chain = true)
@NoArgsConstructor
public class ProdTradeEntity {

    @Id
    private Long id;

    private String symbol;

    private String timeframe;

    private String type;

    private Double entry;

    private Double sl;

    private Double tp;

    private Double lots;

    private Double spread;

    private LocalDateTime stamp;

    private String activated;

    private Double openprice;

    private Double swap;

    private Double profit;

    private String closed;

    private Double commision;

    private String strategy;

    private Double exit;

}