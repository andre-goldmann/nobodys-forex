package jdg.digital.apigateway.config;

import lombok.ToString;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.core.authority.AuthorityUtils;

@ToString
public class JwtAuthentication extends AbstractAuthenticationToken {

    private final AccessToken accessToken;

    public JwtAuthentication(AccessToken accessToken) {
        //
        super(AuthorityUtils.createAuthorityList("ROLE_USER"));
        //super(accessToken.getAuthorities());
        //accessToken.getAuthorities().forEach(this::setAuthenticated);
        this.accessToken = accessToken;
        setAuthenticated(true);
    }

    @Override
    public Object getCredentials() {
        return accessToken.getValue();
    }

    @Override
    public Object getPrincipal() {
        return accessToken.getUsername();
    }

    /*@Override
    public boolean isAuthenticated() {
        return true;
    }

    @Override
    public void setAuthenticated(boolean authenticated) {
        throw new UnsupportedOperationException();
    }*/
}
