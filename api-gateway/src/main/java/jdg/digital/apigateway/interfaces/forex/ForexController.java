package jdg.digital.apigateway.interfaces.forex;

import jakarta.servlet.http.HttpServletRequest;
import jdg.digital.api_interface.*;
import jdg.digital.apigateway.domain.*;
import jdg.digital.apigateway.interfaces.NavbarData;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.socket.WebSocketHandler;
import reactor.core.publisher.Mono;

import java.util.List;

@RestController
@RequestMapping("forex")
@Slf4j
public class ForexController {

    @Autowired
    private TokenValidationService tokenValidationService;

    @Autowired
    private WebSocketHandler forexHandler;

    @Autowired
    private TradeStatsService tradeStatsService;

    @Autowired
    private ForexService forexService;

    @GetMapping("/signals/{env}")
    //@PreAuthorize("isAuthenticated() and hasRole('USER')")
    // Funktioniert
    //@PreAuthorize("isAuthenticated()")
    // Funktioniert nicht
    // Funktioniert, wenn manuell in der JwtAuthentication hinzugefügt
    // @PreAuthorize("hasRole('USER')")
    //@PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<List<Signal>> getSignals(
            @PathVariable("env") final String env) {
        // kann man machen, aber @PreAuthorize prüft schon alles
        //Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        //log.info("auth: {}, {}", auth, auth.getAuthorities());
        return this.forexService.getSignals(env);
    }

    @GetMapping("/signals/ignored")
    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<List<Signal>> getIgnoredSignals() {
        return this.forexService.getIgnoredSignals();
    }

    @DeleteMapping("/signals/ignored/delete")
    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<Void> deleteIgnoredSignal(@RequestParam String json) {
        return this.forexService.deleteIgnoredSignal(json);
    }

    @PostMapping("/trades/updatehistory/{env}")
    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<String> updatehistory(@PathVariable("env") final String env, @RequestBody TradeHistoryUpdate trade) {
        return this.forexService.updateHistory(env, trade);
    }

    @PutMapping("/trades/update/{env}")
    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<Trade> updateTrade(@PathVariable("env") final String env, @RequestBody Trade trade) {
        return this.forexService.updateTrade(env, trade);
    }

    @GetMapping("/trades/statsforlastntrades")
    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<List<StatsPerProdTrade>> getStatsForLastNTrades() {
        return this.forexService.getStatsForLastNTrades();
    }

    @GetMapping("/trades/positive-profit")
    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<List<Trade>> getTradesWithPositiveProfit(@RequestParam SymbolEnum symbol, @RequestParam StrategyEnum strategy) {
        return this.forexService.getTradesWithPositiveProfit(symbol, strategy);
    }

    @GetMapping("/trades/negative-profit")
    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<List<Trade>> getTradesWithNegativeProfit(@RequestParam SymbolEnum symbol, @RequestParam StrategyEnum strategy) {
        return this.forexService.getTradesWithNegativeProfit(symbol, strategy);
    }

    @GetMapping("/trades/tradestats/{env}")
    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    public Mono<TradeStat[]> getTradeStats(@PathVariable("env") final String env) {
        return this.tradeStatsService.getTradeStats(env);
    }

    // this is always accessible
    @GetMapping("/routes")
    public ResponseEntity<List<NavbarData>> getRoutes(){
        //final String authorization = request.getHeader("authorization");
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
                NavbarData.builder()
                        .routeLink("signals")
                        .icon("fa-solid fa-signal")
                        .label("Signals")
                        .build(),
                NavbarData.builder()
                        .routeLink("trades")
                        .icon("fa-solid fa-exchange")
                        .label("Trades")
                        .build(),
                NavbarData.builder()
                        .routeLink("stats")
                        .icon("fa-solid fa-chart-bar")
                        .label("Stats")
                        .build(),
                NavbarData.builder()
                        .routeLink("regression")
                        .icon("fa-solid fa-chart-line")
                        .label("Regression")
                        .build(),
                NavbarData.builder()
                        .routeLink("playground")
                        .icon("fa-solid fa-tag")
                        .label("Playground")
                        .build(),
                // TODO signals, trades, stats, regression, etc
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

    @PreAuthorize("isAuthenticated() and hasRole('ROLE_USER')")
    @GetMapping("/symbols")
    public ResponseEntity<List<String>> getSymbols(HttpServletRequest request){

        //final String authorization = request.getHeader("authorization");
        //if(authorization == null || authorization.isEmpty()){
//            return ResponseEntity.badRequest().build();
        //}
        final StringBuilder headersBuilder = new StringBuilder();
        // Get all header names and print them
        request.getHeaderNames().asIterator().forEachRemaining(headerName -> {
            headersBuilder.append(headerName).append(": ").append(request.getHeader(headerName)).append("\n");
        });
        log.info(headersBuilder.toString());

        /*log.info(request.getHeader("origin"));
        log.info(request.getHeader("authorization").replace("Bearer ", ""));
        log.info(request.getHeader("content-type"));
        log.info(request.getHeader("accept"));*/
        // Same exception as Spring throws, this happens because there seem to be issues with the
        // keystore beeing used
        //log.info("is valid: {}",this.tokenValidationService.isValidToken(request.getHeader("authorization").replace("Bearer ", "")));
        return ResponseEntity.ok(List.of("USDCAD", "EURUSD", "GBPUSD", "JPYUSD"));
        // actually not working
        /*if (authentication != null && authentication.getPrincipal() instanceof Jwt) {
            final Jwt jwt = (Jwt) authentication.getPrincipal();
            final String token = jwt.getTokenValue();
            if(this.tokenValidationService.isValidToken(token)) {
                // Now you have the bearer token
                //return ResponseEntity.badRequest().build();
                return ResponseEntity.ok(List.of("USDCAD", "EURUSD", "GBPUSD", "JPYUSD"));
            }
            log.error("Authenticated but token is invalid!!!");
            return ResponseEntity.badRequest().build();

        } else {
            // No bearer token found
            //No bearer token found
            if(authentication != null && authentication.getPrincipal() != null) {
                log.error("Not authenticated: {}", authentication.getPrincipal());
            }else {
                log.error("Not authenticated: {}", authentication);
            }
            return ResponseEntity.badRequest().build();
        }*/
    }
}
