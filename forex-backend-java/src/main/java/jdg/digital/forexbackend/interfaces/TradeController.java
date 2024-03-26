package jdg.digital.forexbackend.interfaces;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TradeController {

    @GetMapping("trades")
    public String getTrades(){
        return "Hello World";
    }
}
