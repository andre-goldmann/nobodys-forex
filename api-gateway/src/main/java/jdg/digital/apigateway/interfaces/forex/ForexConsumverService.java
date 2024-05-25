package jdg.digital.apigateway.interfaces.forex;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketHandler;

@Service
@Slf4j
public class ForexConsumverService {

    @Autowired
    private WebSocketHandler forexHandler;

    @KafkaListener(topics = "signals", groupId = "forex")
    public void listen(String message) {
        log.info("Received message: {}", message);
        if(this.forexHandler instanceof ForexHandler){
            ((ForexHandler) this.forexHandler).sendMessage(new TextMessage(message));
        }
    }
}
