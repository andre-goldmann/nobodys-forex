package jdg.digital.forexbackend.domain.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

@Table("\"IgnoredSignals\"")
@Getter
@Setter
@ToString
@Accessors(chain = true)
@NoArgsConstructor
public class IgnoredSignalEntity {

    @Id
    private Integer id;

    private String json;

    private String reason;

}
