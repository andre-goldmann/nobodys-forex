package jdg.digital.apigateway.interfaces;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("forex")
@Slf4j
public class ForexController {

    @GetMapping("/symbols")
    public ResponseEntity<List<String>> getSymbols(){
        log.info("getSymbols...");
        return ResponseEntity.ok(List.of("USDCAD", "EURUSD", "GBPUSD", "JPYUSD"));
    }
}
