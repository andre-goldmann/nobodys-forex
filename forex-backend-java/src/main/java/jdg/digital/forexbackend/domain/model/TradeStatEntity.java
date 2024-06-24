package jdg.digital.forexbackend.domain.model;


import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

@Table(name= "\"Trades\"")
@Getter
@Setter
@ToString
@Accessors(chain = true)
@NoArgsConstructor
public class TradeStatEntity {

    @Id
    private Integer id;

    private String symbol;

    private String strategy;

    private Double profit;

    private Integer loses;

    private Integer wins;

    private Integer total;

    private Double winpercentage;
}
