package jdg.digital.forexbackend.utils;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;

import java.io.IOException;
import java.time.OffsetDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

public class CustomOffsetDateTimeDeserializer extends JsonDeserializer<OffsetDateTime> {
    // 2024-03-19 14:45:05.110579 +00:00
    private DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSSSSS XXX");

    @Override
    public OffsetDateTime deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
        try {
            return OffsetDateTime.parse(p.getValueAsString(), formatter);
        } catch (DateTimeParseException e){
            return OffsetDateTime.now();
        }
    }

}
