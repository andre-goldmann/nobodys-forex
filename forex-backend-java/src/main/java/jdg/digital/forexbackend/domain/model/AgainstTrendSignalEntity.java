package jdg.digital.forexbackend.domain.model;

import lombok.*;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

@Table("AgainstTrendSignals")
@Getter
@Setter
@ToString
@Accessors(chain = true)
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AgainstTrendSignalEntity {

    @Id
    private Long id;

    private String symbol;

    private String timeframe;

    private String strategy;

    private String type;

    private String timestamp;

}
