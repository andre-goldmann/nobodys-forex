import {computed, Inject, inject, Injectable, signal} from '@angular/core';

import {debounceTime, EMPTY, filter, map, Observable, of} from "rxjs";
import {AuthConfig, OAuthService} from "angular-oauth2-oidc";
import {APP_CONFIG, AppConfig} from "@angular-projects/app-config";
import {HttpClient} from "@angular/common/http";

type LoginEventType = 'token_received';

export class LoginEvent {
  constructor(readonly type: LoginEventType) { }
}

const useSilentRefreshForCodeFlow = false;

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  events: Observable<LoginEvent>;

  private AUTH_CONFIG: AuthConfig = {

    issuer: this.appConfig.keycloakHost,

    // URL of the SPA to redirect the user to after login
    redirectUri: this.appConfig.webHost,

    // The SPA's id. The SPA is registerd with this id at the auth-server
    // clientId: 'server.code',
    clientId: this.appConfig.clientId,

    responseType: 'code',// starts the CodeFlow
    //responseType: 'token',// starts the ImplicitFlow

    // set the scope for the permissions the client should request
    // The first four are defined by OIDC.
    // Important: Request offline_access to get a refresh token
    // The api scope is a usecase specific one
    scope: useSilentRefreshForCodeFlow
      ? 'openid profile email roles'
      : 'openid profile email offline_access roles',

    showDebugInformation: true,

    oidc: true,

    disablePKCE: true,

    requireHttps: this.appConfig.requireHttps,

    // ^^ Please note that offline_access is not needed for silent refresh
    // At least when using idsvr, this even prevents silent refresh
    // as idsvr ALWAYS prompts the user for consent when this scope is
    // requested

    // This is needed for silent refresh (refreshing tokens w/o a refresh_token)
    // **AND** for logging in with a popup
    silentRefreshRedirectUri: `${window.location.origin}/silent-refresh.html`,

    useSilentRefresh: useSilentRefreshForCodeFlow,

    sessionChecksEnabled: false,

    timeoutFactor: 0.01,

    //clearHashAfterLogin: true,

    //requestAccessToken:true,
    //useHttpBasicAuth: false,

    tokenEndpoint:  this.appConfig.keycloakHost + '/protocol/openid-connect/token',
    userinfoEndpoint: this.appConfig.keycloakHost + "/protocol/openid-connect/userinfo",
    revocationEndpoint: this.appConfig.keycloakHost + "/protocol/openid-connect/revoke"
  }

  constructor(
    @Inject(APP_CONFIG) private appConfig: AppConfig,
    private oauthService: OAuthService,
    private http: HttpClient) {

    this.events = this.oauthService.events
      .pipe(
        filter(e => e.type === 'token_received' || (e.type === 'discovery_document_loaded' && this.oauthService.hasValidAccessToken())),
        map(_e => new LoginEvent('token_received')),
        debounceTime(500)
      );
  }

  login() {
    this.oauthService.initLoginFlow();
    return EMPTY;
  }

  fetchToken(code:string){

    const parameters: { [key: string]: any } = {
      client_id: this.appConfig.clientId,
      client_secret: this.appConfig.clientSecret,
      redirect_uri: this.appConfig.webHost,
      code: code
    };
    return this.oauthService.fetchTokenUsingGrant('authorization_code', parameters);
  }

  init() {
    this.configureCodeFlow();
  }

  private configureCodeFlow() {
    this.oauthService.configure(this.AUTH_CONFIG);

    this.oauthService.loadDiscoveryDocumentAndTryLogin()
      .then(() => {
        this.oauthService.setupAutomaticSilentRefresh()
        //this.initialized$.next(void 0);
        //this.initialized$.complete();
      }, () => {
        //this.initialized$.next();
        //this.initialized$.complete();
      });
  }

  logout() {
    this.oauthService.logOut();
  }

  hasValidAccessToken() {
    return this.oauthService.hasValidIdToken();
  }

  hasValidIdToken() {
    return this.oauthService.hasValidIdToken();
  }

  getAccessToken() {
    return this.oauthService.hasValidAccessToken() ? this.oauthService.getAccessToken() : null;
  }

  userProfile(){
    return this.oauthService.loadUserProfile();
  }
}
