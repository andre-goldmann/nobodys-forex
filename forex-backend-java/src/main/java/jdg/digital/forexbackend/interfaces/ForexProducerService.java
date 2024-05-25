package jdg.digital.forexbackend.interfaces;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class ForexProducerService {

    private final KafkaTemplate<String, String> kafkaTemplate;

    @Autowired
    public ForexProducerService(final KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendMessage(String topic, String message) {
        this.kafkaTemplate.send(topic, message);
    }
}
