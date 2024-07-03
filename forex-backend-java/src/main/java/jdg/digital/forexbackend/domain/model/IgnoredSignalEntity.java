package jdg.digital.forexbackend.domain.model;

import lombok.*;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

@Table("IgnoredSignals")
@Getter
@Setter
@ToString
@Accessors(chain = true)
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class IgnoredSignalEntity {

    @Id
    private Integer id;

    private String symbol;

    private String strategy;

    private String timeframe;

    private int loses;

    private int wins;

    private int total;

    private String info;

}
