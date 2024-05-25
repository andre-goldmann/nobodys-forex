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

    /*@Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                .authorizeRequests()
                .anyRequest().permitAll()
                .and()
                .csrf().disable(); // Disable CSRF for simplicity, you might need to enable it depending on your application's requirements
    }*/

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
        /*http.csrf(AbstractHttpConfigurer::disable)
                .authorizeHttpRequests(authorizationManagerRequestMatcherRegistry ->
                        authorizationManagerRequestMatcherRegistry.requestMatchers(HttpMethod.DELETE).hasRole("ADMIN")
                                .requestMatchers("/admin/**").hasAnyRole("ADMIN")
                                .requestMatchers("/user/**").hasAnyRole("USER", "ADMIN")
                                .requestMatchers("/login/**").permitAll()
                                .anyRequest().authenticated())
                .httpBasic(Customizer.withDefaults())
                .sessionManagement(httpSecuritySessionManagementConfigurer -> httpSecuritySessionManagementConfigurer.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
        */

        http.authorizeHttpRequests(authz -> authz
                        .requestMatchers("/forex/**").permitAll()
                        //.requestMatchers("/h2/**").permitAll()
                        .anyRequest().permitAll())
                // TODO remove this line
                .csrf(csrf -> csrf.disable())
                .cors(cors -> cors.disable());
        /*http
                .authorizeRequests()
                .anyRequest().permitAll()
                .and()
                //.csrf(csrf -> csrf.disable())
                .cors(cors -> cors.disable());*/
        return http.build();
    }

    /*@Bean
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
    }*/
}
