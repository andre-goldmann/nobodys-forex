package jdg.digital.apigateway.interfaces.financialdataanalysis;

import jakarta.servlet.http.HttpServletRequest;
import jdg.digital.apigateway.interfaces.NavbarData;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("financialdataanalysis")
@Slf4j
public class FinancialDataAnalysisController {
    @GetMapping("/routes")
    public ResponseEntity<List<NavbarData>> getRoutes(Authentication authentication, HttpServletRequest request){
        final String authorization = request.getHeader("authorization");
        /*if(authorization == null || authorization.isEmpty()){
            return ResponseEntity.badRequest().build();
        }*/
        // TODO move this code here to single microservice
        return ResponseEntity.ok(List.of(
                NavbarData.builder()
                        .routeLink("dashboard")
                        .icon("fa-solid fa-house")
                        .label("Dashboard")
                        .build(),
                /*NavbarData.builder()
                        .routeLink("pricing")
                        .icon("fa-solid fa-tag")
                        .label("Pricing")
                        .build(),
                NavbarData.builder()
                        .routeLink("charts")
                        .icon("fa-solid fa-chart-simple")
                        .label("Charts")
                        .build(),
                NavbarData.builder()
                        .routeLink("admin")
                        .icon("fa-solid fa-gear")
                        .label("Admin")
                        .build(),*/
                NavbarData.builder()
                        .routeLink("logout")
                        .icon("fa-solid fa-arrow-right-from-bracket")
                        .label("Logout")
                        .build()
        ));
    }
}
