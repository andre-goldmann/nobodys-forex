package jdg.digital.apigateway.config;

import java.nio.charset.StandardCharsets;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.AuthenticationConverter;
import org.springframework.security.web.authentication.AuthenticationFailureHandler;
import org.springframework.security.web.authentication.AuthenticationFilter;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;

class RobotAuthenticationFilter extends AuthenticationFilter {

    private final static String HEADER_NAME = "x-robot-password";
    private static final AuthenticationConverter authenticationConverter = req -> {
        /*if (Collections.list(req.getHeaderNames()).contains(HEADER_NAME)) {
            return "";//RobotAuthentication.unauthenticated(req.getHeader(HEADER_NAME));
        }
        return null;*/

        // this is set before within TokenRequiredFilter
        return SecurityContextHolder.getContext().getAuthentication();
    };

    private static String extractAuthorizationHeaderAsString(HttpServletRequest request) {
        try {
            return request.getHeader("Authorization");
        } catch (Exception ex){
            throw new InvalidTokenException("There is no Authorization header in a request", ex);
        }
    }

    private final AuthenticationFailureHandler failureHandler = (request, response, exception) -> {
        response.setStatus(HttpStatus.FORBIDDEN.value());
        response.setCharacterEncoding(StandardCharsets.UTF_8.name());
        response.setContentType("text/plain;charset=utf8");
        response.getWriter().write(exception.getMessage());
    };

    private final AuthenticationSuccessHandler successHandler = (request, response, authentication) -> {
        //System.out.printf("Robot %s authenticated successfully! 🤖%n", authentication.getPrincipal());
        //var newContext = SecurityContextHolder.createEmptyContext();
        //newContext.setAuthentication(authentication);
        //SecurityContextHolder.setContext(newContext);
    };

    public RobotAuthenticationFilter(AuthenticationManager authenticationManager) {
        super(authenticationManager, authenticationConverter);
        setFailureHandler(failureHandler);
        setSuccessHandler(successHandler);
    }
}
