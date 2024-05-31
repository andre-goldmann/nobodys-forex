package jdg.digital.forexbackend.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {
    @Bean
    public ObjectMapper mapper() {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.registerModule(new JavaTimeModule());
    }
}
