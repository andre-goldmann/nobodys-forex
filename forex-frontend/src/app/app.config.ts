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

export const SPRING_HOST = 'http://localhost:5000/resource-server';

//export const HOST_HOST = 'http://172.17.134.138:3000';
// Muss ggf. in Keycloak siehe "Valid redirect URIs" geändert werden
export const WEB_HOST = 'http://localhost:4200';
// How to get IP from docker?
//export const WEB_HOST = 'http://172.26.187.22';

export  const KEYCLOACK_HOST = "http://172.26.181.56:8180/auth/realms/school_admininstrator";

export const CLIENT_ID = 'school-admininstrator-client';
// das ist Mist, wie geht das anders?
export const CLIENT_SECRET='PfQER9b4JBjMXOvESdqHFctrJeDll20z';

const useSilentRefreshForCodeFlow = false;

export const AUTH_CONFIG: AuthConfig = {

  requireHttps: false,

  issuer: KEYCLOACK_HOST,

  // URL of the SPA to redirect the user to after login
  redirectUri: window.location.origin,


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
