package jdg.digital.apigateway.interfaces.forex;

public class ClientMessage {
    public String sessionId;
    public String message;

    public ClientMessage(){}
    public ClientMessage(String sessionId, String message){
        this.sessionId = sessionId;
        this.message = message;
    }
}
