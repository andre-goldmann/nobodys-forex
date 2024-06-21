package jdg.digital.forexbackend.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity(securedEnabled = true, jsr250Enabled = true)
//@EnableConfigurationProperties(OAuth2ResourceServerProperties.class)
@Slf4j
public class SecurityConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedMethods("*")
                .allowedOrigins(
                        // For local development
                        "http://localhost:4200",
                        "http://localhost:4300",
                        "https://85.215.32.163",
                        "https://nobodys-forex.vercel.app");
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        http.authorizeHttpRequests(authz -> authz
                        .requestMatchers("/forex/**").permitAll()
                        //.requestMatchers("/h2/**").permitAll()
                        .anyRequest().permitAll());
                // TODO remove this line
                //.csrf(csrf -> csrf.disable())
                //.cors(cors -> cors.disable());
        /*http
                .authorizeRequests()
                .anyRequest().permitAll()
                .and()
                //.csrf(csrf -> csrf.disable())
                .cors(cors -> cors.disable());*/
        return http.build();
    }
}
