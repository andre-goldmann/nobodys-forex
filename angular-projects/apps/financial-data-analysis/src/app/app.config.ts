import {ApplicationConfig, importProvidersFrom} from '@angular/core';

import {HttpClientModule} from "@angular/common/http";
import { environment } from '../environments/environment';
import { getAppConfigProvider } from '@angular-projects/app-config';
import {provideRouter, withInMemoryScrolling, withRouterConfig} from '@angular/router';

import { APP_ROUTES } from './app.routes';
import {BrowserModule} from "@angular/platform-browser";
import {FormsModule} from "@angular/forms";
import {CommonModule} from "@angular/common";
import {provideAnimations} from "@angular/platform-browser/animations";
import {provideHttpClient, withInterceptors, withInterceptorsFromDi} from "@angular/common/http";
import {provideOAuthClient} from "angular-oauth2-oidc";
import {authenticationInterceptor} from "@angular-projects/utils";


export const appConfig: ApplicationConfig = {
  providers: [
    getAppConfigProvider(environment),
    /*provideMatomo(
      {
        siteId: 1,
        trackerUrl: "http://172.26.181.56:8080/"
      }, // Your configuration
      withRouter()
    ),*/
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
      /*OAuthModule.forRoot({
        resourceServer: {
          allowedUrls: ['http://172.26.181.56:4000/spring'],
          sendAccessToken: true
        }})*/
    ),
    provideAnimations(),
    provideHttpClient(
      withInterceptorsFromDi(),
      withInterceptors([authenticationInterceptor])
    ),
    provideOAuthClient()
  ],
};