package jdg.digital.apigateway.config;

import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

public class JwtAuthenticationProvider implements AuthenticationProvider {

    @Override
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        // Implement your authentication logic here.
        // For example, you might validate the JWT token and create an authenticated Authentication object.

        //JwtAuthentication jwtAuthentication = (JwtAuthentication) authentication;
        // Validate the JWT token and create an authenticated Authentication object.

        return authentication;
    }

    @Override
    public boolean supports(Class<?> authentication) {
        // This method should return true if this AuthenticationProvider supports the provided Authentication class.
        return JwtAuthentication.class.isAssignableFrom(authentication);
    }
}