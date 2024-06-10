package jdg.digital.apigateway.config;

import com.auth0.jwk.JwkProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.logout.LogoutFilter;
import org.springframework.context.ApplicationListener;
import org.springframework.security.authentication.event.AuthenticationSuccessEvent;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import static org.springframework.security.config.Customizer.withDefaults;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity(securedEnabled = true, jsr250Enabled = true)
public class SecurityConfig implements WebMvcConfigurer {

    @Value("${keycloak.jwk}")
    private String jwkProviderUrl;
    // does not work anymore
    public static final String[] ALLOW_ORIGINS = {
            "http://localhost:4200",
            "http://localhost:4300",
            "https://85.215.32.163",
            "https://nobodys-forex.vercel.app"
    };

    @Override
    public void addCorsMappings(final CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedMethods("*")
                .allowedOrigins(ALLOW_ORIGINS);
    }

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {

        return http
                .authorizeHttpRequests(
                        authorizeHttp -> {
                            // Allow routes to be accessed without authentication
                            // does not work
                            //authorizeHttp.requestMatchers("/routes").permitAll();
                            // does not work
                            //authorizeHttp.requestMatchers("/forex/routes").permitAll();
                            // does not work, but I also do not want to give access to this endpoint
                            //authorizeHttp.requestMatchers("/api/forex/routes").permitAll();
                            authorizeHttp.requestMatchers("/api/forex/signals/dev").permitAll();
                            authorizeHttp.anyRequest().authenticated();
                        }
                )
                // this part is need otherwise there is an Access Denied error
                .with(new RobotAccountConfigurer(), withDefaults())
                //.addFilterBefore(new ForbiddenFilter(), LogoutFilter.class) // filter before auth/logout
                .addFilterBefore(new TokenRequiredFilter(jwtTokenValidator(keycloakJwkProvider())), LogoutFilter.class)
                .authenticationProvider(new JwtAuthenticationProvider())
                .build();
    }

    @Bean
    ApplicationListener<AuthenticationSuccessEvent> successListener() {
        return event -> {
            /*System.out.println("🎉 [%s] %s".formatted(
                    event.getAuthentication().getClass().getSimpleName(),
                    event.getAuthentication().getName()
            ));*/
            //TODO add some other message here
        };
    }

    @Bean
    public JwtTokenValidator jwtTokenValidator(JwkProvider jwkProvider) {
        return new JwtTokenValidator(jwkProvider);
    }

    @Bean
    public JwkProvider keycloakJwkProvider() {
        return new KeycloakJwkProvider(jwkProviderUrl);
    }

}
