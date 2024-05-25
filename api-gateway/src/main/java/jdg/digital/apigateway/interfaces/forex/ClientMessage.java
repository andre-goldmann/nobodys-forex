package jdg.digital.apigateway.interfaces.forex;

public class ClientMessage {
    public String sessionId;
    public String message;

    public ClientMessage(){}
    public ClientMessage(final String sessionId, final String message){
        this.sessionId = sessionId;
        this.message = message;
    }
}
