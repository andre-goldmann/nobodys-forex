package jdg.digital.apigateway.interfaces;

import lombok.*;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class NavbarData {
    private String routeLink;
    private String icon;
    private String label;
}
