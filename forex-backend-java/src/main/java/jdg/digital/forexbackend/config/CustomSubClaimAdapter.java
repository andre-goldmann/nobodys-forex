package jdg.digital.forexbackend.config;

import org.springframework.core.convert.converter.Converter;
import org.springframework.security.oauth2.jwt.MappedJwtClaimSetConverter;

import java.util.Collections;
import java.util.Map;
import java.util.Objects;

public class CustomSubClaimAdapter implements Converter<Map<String, Object>, Map<String, Object>> {

    private final MappedJwtClaimSetConverter delegate = MappedJwtClaimSetConverter.withDefaults(Collections.emptyMap());

    private final String claimName;

    public CustomSubClaimAdapter(final String claimName) {
        this.claimName = Objects.requireNonNull(claimName);
    }

    @Override
    public Map<String, Object> convert(final Map<String, Object> claims) {
        final Map<String, Object> convertedClaims = this.delegate.convert(claims);

        if (convertedClaims != null) {
            final String customClaim = (String) convertedClaims.get(this.claimName);
            convertedClaims.put("sub", customClaim);
        }

        return convertedClaims;
    }

}