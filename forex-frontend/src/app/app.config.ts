import {ApplicationConfig, importProvidersFrom} from '@angular/core';
import {provideRouter, withInMemoryScrolling, withRouterConfig} from '@angular/router';

import { APP_ROUTES } from './app.routes';
import {BrowserModule} from "@angular/platform-browser";
import {FormsModule} from "@angular/forms";
import {CommonModule} from "@angular/common";
import {provideAnimations} from "@angular/platform-browser/animations";
import {provideHttpClient, withInterceptors, withInterceptorsFromDi} from "@angular/common/http";
import {AuthConfig, OAuthModule, provideOAuthClient} from "angular-oauth2-oidc";
import {provideMatomo, withRouter} from "ngx-matomo-client";
import {authenticationInterceptor} from "./guards/auth.interceptor";

export const NODE_HOST = 'http://nodebackend';

//export const SPRING_HOST = 'http://127.0.01:5080/resource-server';
export const SPRING_HOST = 'https://85.215.32.163:5080/resource-server';
// Prod
//export const API_GATEWAY = 'https://85.215.32.163:9080/api';
//export const API_GATEWAY = 'https://172.25.138.181:9080/api';
export const API_GATEWAY = 'http://localhost:9080/api';

// Muss ggf. in Keycloak siehe "Valid redirect URIs" geändert werden
export const WEB_HOST = window.location.origin;//'http://172.31.138.212';
// How to get IP from docker?
//export const WEB_HOST = 'http://172.26.187.22';
//http://localhost:4200/login/oauth2/code/keycloak
// Prod
//export  const KEYCLOACK_HOST = "https://85.215.32.163:8443/realms/forex_admininstrator";
export  const KEYCLOACK_HOST = "https://172.25.138.181:8443/realms/forex_admininstrator";

export const CLIENT_ID = 'forex_admininstrator_client';
// das ist Mist, wie geht das anders?
// Prod
//export const CLIENT_SECRET='L7YFcYYKDDpIG6dvBtISskp40O8RiyXd';
export const CLIENT_SECRET='1qFzfPvMEei1ksMIbnC9vkDyxihxtc5P';

const useSilentRefreshForCodeFlow = false;

export const AUTH_CONFIG: AuthConfig = {

  requireHttps: false,

  issuer: KEYCLOACK_HOST,

  // URL of the SPA to redirect the user to after login
  redirectUri: WEB_HOST,

  // The SPA's id. The SPA is registerd with this id at the auth-server
  // clientId: 'server.code',
  clientId: CLIENT_ID,

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

  tokenEndpoint:  KEYCLOACK_HOST + '/protocol/openid-connect/token',
  userinfoEndpoint: KEYCLOACK_HOST + "/protocol/openid-connect/userinfo",
};
/*export function storageFactory() : OAuthStorage {
  return localStorage
}*/

export const appConfig: ApplicationConfig = {
  providers: [
    // { provide: OAuthStorage, useFactory: storageFactory },
    provideMatomo(
      {
        siteId: 1,
        trackerUrl: "http://172.26.181.56:8080/"
      }, // Your configuration
      withRouter()
    ),
    provideRouter(
      APP_ROUTES,
      withInMemoryScrolling({
        scrollPositionRestoration: 'disabled',
      }),
      withRouterConfig({
        onSameUrlNavigation: 'reload',
      })
    ),
    importProvidersFrom(
      BrowserModule,
      FormsModule,
      CommonModule,
      OAuthModule.forRoot({
        resourceServer: {
          allowedUrls: ['http://172.26.181.56:4000/spring'],
          sendAccessToken: true
        }})

    ),
    provideAnimations(),
    provideHttpClient(
      withInterceptorsFromDi(),
      withInterceptors([authenticationInterceptor])
    ),
    provideOAuthClient()
  ],
};
