import {Inject, inject, Injectable} from '@angular/core';

import {EMPTY, Observable, of} from "rxjs";
import {Credentials} from "../models/credentials";
import {Router} from "@angular/router";
import {OAuthService} from "angular-oauth2-oidc";
import {HttpClient} from "@angular/common/http";
import {AppConfig} from "@angular-projects/app-config";

export type LoginStatus = 'pending' | 'authenticating' | 'success' | 'error';

interface LoginState {
  status: LoginStatus;
}

const useSilentRefreshForCodeFlow = false;

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  private router:Router = inject(Router);

  constructor(
    @Inject(APP_CONFIG) private appConfig: AppConfig,
    private oauthService: OAuthService,
    private http:HttpClient) {
  }


  createAccount(credentials: Credentials):Observable<void> {
    return EMPTY;
  }

  login() {
    console.info("Start login...");

    this.oauthService.loadDiscoveryDocumentAndLogin()
      .then(() => {
        console.info("then loadDiscoveryDocumentAndLogin executed");
        this.oauthService.setupAutomaticSilentRefresh();

      }, () => {
        console.info("loadDiscoveryDocumentAndLogin executed");

      });

    this.oauthService.discoveryDocumentLoaded$.subscribe(e =>{
      console.info(e);
    });

    return EMPTY;
  }

  fetchToken(code:string){

    const parameters: { [key: string]: any } = {
      client_id: this.appConfig.clientId,
      client_secret: this.appConfig.clientSecret,
      redirect_uri: this.appConfig.webHost,
      code: code
    };

    this.oauthService.fetchTokenUsingGrant('authorization_code', parameters)
      .then(e => {
        console.info("Got token...");
        this.router.navigate(["/dashboard"]);
      });
  }

  init() {

    this.configureCodeFlow();

    // Automatically load user profile
    this.oauthService.events
      //.pipe(filter((e) => e.type === 'token_received'))
      .subscribe((value) => {
        console.info("Event from oauthService" + value.type);

        const scopes = this.oauthService.getGrantedScopes();
        console.info('scopes', scopes);
      });
  }

  private configureCodeFlow() {
    this.oauthService.configure(
      {

        requireHttps: false,

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

        // ^^ Please note that offline_access is not needed for silent refresh
        // At least when using idsvr, this even prevents silent refresh
        // as idsvr ALWAYS prompts the user for consent when this scope is
        // requested

        // This is needed for silent refresh (refreshing tokens w/o a refresh_token)
        // **AND** for logging in with a popup
        silentRefreshRedirectUri: `${window.location.origin}/silent-refresh.html`,

        useSilentRefresh: useSilentRefreshForCodeFlow,

        showDebugInformation: true,

        sessionChecksEnabled: false,

        timeoutFactor: 0.01,

        clearHashAfterLogin: true,

        oidc: true,

        //requestAccessToken:true,
        useHttpBasicAuth: false,

        disablePKCE: true,

        tokenEndpoint:  this.appConfig.keycloakHost + '/protocol/openid-connect/token',
        userinfoEndpoint: this.appConfig.keycloakHost + "/protocol/openid-connect/userinfo",
      }
    );
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

}
