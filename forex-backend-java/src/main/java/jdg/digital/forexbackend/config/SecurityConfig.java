package jdg.digital.forexbackend.config;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.security.oauth2.resource.OAuth2ResourceServerProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.oauth2.jwt.*;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Collections;

@Configuration
@EnableWebSecurity
@EnableConfigurationProperties(OAuth2ResourceServerProperties.class)
@Slf4j
public class SecurityConfig {
    @Bean
    public SecurityFilterChain defaultSecurityFilterChain(final HttpSecurity http, @Autowired(required = false) final OAuth2ResourceServerProperties oAuth2ResourceServerProperties) throws Exception {
        this.configureAuthorization(http);
        this.configureCors(http);
        final var jwtDecoder = this.jwtDecoder(oAuth2ResourceServerProperties);

        if (oAuth2ResourceServerProperties.getJwt() != null && (StringUtils.isNotBlank(oAuth2ResourceServerProperties.getJwt().getIssuerUri()) || StringUtils.isNotBlank(oAuth2ResourceServerProperties.getJwt().getJwkSetUri()))
        ) {

            http.oauth2ResourceServer().jwt().decoder(jwtDecoder);
        }

        return http.build();
    }

    void configureAuthorization(final HttpSecurity httpSecurity) throws Exception {
        httpSecurity
                .authorizeHttpRequests()
                .requestMatchers("/actuator/prometheus").permitAll()
                .requestMatchers("/actuator/prometheus/**").permitAll()
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/actuator/health/**").permitAll()
                .requestMatchers("/actuator/info").permitAll()
                .requestMatchers("/actuator/info/**").permitAll()
                .requestMatchers("/swagger-ui/").permitAll()
                .requestMatchers("/swagger-ui/**").permitAll()
                .requestMatchers("/swagger-resources").permitAll()
                .requestMatchers("/swagger-resources/**").permitAll()
                .requestMatchers("/v3/api-docs").permitAll()
                .requestMatchers("/v3/api-docs/**").permitAll()
                .anyRequest().authenticated();
    }

    // CORS (Cross-Origin Resource Sharing)
    void configureCors(final HttpSecurity httpSecurity) throws Exception {
        httpSecurity.cors()
                .configurationSource(this.corsConfigurationSource());
    }

    private CorsConfigurationSource corsConfigurationSource() {
        final CorsConfiguration configuration = new CorsConfiguration();
        configuration.applyPermitDefaultValues();
        configuration.setAllowCredentials(true);
        // TODO remove this
        configuration.setAllowedOriginPatterns(Collections.singletonList("*"));
        final UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }

    private JwtDecoder jwtDecoder(OAuth2ResourceServerProperties oAuth2ResourceServerProperties) {
        var jwt = oAuth2ResourceServerProperties.getJwt();

        final var jwtDecoder = NimbusJwtDecoder.withJwkSetUri(jwt.getJwkSetUri()).build();
        jwtDecoder.setClaimSetConverter(new CustomSubClaimAdapter("uuid"));
        return jwtDecoder;
    }
}
