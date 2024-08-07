package jdg.digital.apigateway.interfaces.forex;

import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;


public class ForexHandler extends TextWebSocketHandler {

    private final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();

    @Override
    public void afterConnectionEstablished(final WebSocketSession session) {
        sessions.put(session.getId(), session);
    }

    @Override
    public void handleTextMessage(final WebSocketSession session, final TextMessage message) {
        System.out.println("Received message: " + message.getPayload());
    }

    public void sendMessage(final TextMessage message) {
        this.sessions.forEach((sessionId, session) -> {
            if (session != null && session.isOpen()) {
                try {
                    session.sendMessage(message);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });

    }
}
