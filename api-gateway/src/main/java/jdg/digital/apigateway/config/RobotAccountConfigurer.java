package jdg.digital.apigateway.config;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.web.access.intercept.AuthorizationFilter;

class RobotAccountConfigurer extends AbstractHttpConfigurer<RobotAccountConfigurer, HttpSecurity> {

    /*@Override
    public void init(HttpSecurity http) {
        http.authenticationProvider(
                //new RobotAuthenticationProvider()
                new JwtAuthenticationProvider()
        );
    }*/

    @Override
    public void configure(HttpSecurity http) {
        var authManager = http.getSharedObject(AuthenticationManager.class);
        // this also needed to avoid Access Denied error
        http.addFilterBefore(
                new RobotAuthenticationFilter(authManager),
                AuthorizationFilter.class
        );
    }
}