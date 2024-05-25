package jdg.digital.apigateway.config;

import jdg.digital.apigateway.interfaces.forex.ForexHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

import static jdg.digital.apigateway.config.SecurityConfig.ALLOW_ORIGINS;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(final WebSocketHandlerRegistry registry) {
        registry.addHandler(forexHandler(), "/forexHandler")
                .setAllowedOrigins(ALLOW_ORIGINS);
    }

    @Bean
    public WebSocketHandler forexHandler() {
        return new ForexHandler();
    }

}
