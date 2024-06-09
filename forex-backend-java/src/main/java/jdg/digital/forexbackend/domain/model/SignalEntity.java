package jdg.digital.forexbackend.domain.model;


import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

import java.time.OffsetDateTime;

@Table(name= "\"Trades\"")
@Getter
@Setter
@ToString
@Accessors(chain = true)
@NoArgsConstructor
public class SignalEntity {

    @Id
    private Integer id;

    private String symbol;

    private String strategy;

    private String timeframe;

    private String type;

    private Double entry;

    private Double sl;

    private Double tp;

    private Double lots;

    private OffsetDateTime stamp;

}
