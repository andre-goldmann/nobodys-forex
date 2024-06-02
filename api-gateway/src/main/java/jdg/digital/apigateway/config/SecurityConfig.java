package jdg.digital.apigateway.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.logout.LogoutFilter;
import org.springframework.context.ApplicationListener;
import org.springframework.security.authentication.event.AuthenticationSuccessEvent;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import static org.springframework.security.config.Customizer.withDefaults;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity(securedEnabled = true, jsr250Enabled = true)
public class SecurityConfig implements WebMvcConfigurer {

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
                            // Allow origins
                            //authorizeHttp.requestMatchers("/").permitAll();
                            //authorizeHttp.requestMatchers("/favicon.svg").permitAll();
                            //authorizeHttp.requestMatchers("/css/*").permitAll();
                            //authorizeHttp.requestMatchers("/error").permitAll();
                            authorizeHttp.anyRequest().authenticated();
                        }
                )
                .oauth2Login(withDefaults())
                .with(new RobotAccountConfigurer(), withDefaults())
                .addFilterBefore(new ForbiddenFilter(), LogoutFilter.class) // filter before auth/logout
                .authenticationProvider(new DanielAuthenticationProvider())
                .build();
    }

    @Bean
    UserDetailsService userDetailsService(){
        return new InMemoryUserDetailsManager(
                User.withUsername("user")
                        .password("{noop}password")
                        .roles("user")
                        .build()
        );
    }

    @Bean
    ApplicationListener<AuthenticationSuccessEvent> successListener() {
        return event -> {
            System.out.println("🎉 [%s] %s".formatted(
                    event.getAuthentication().getClass().getSimpleName(),
                    event.getAuthentication().getName()
            ));
        };
    }


}
