import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import {provideAnimations} from "@angular/platform-browser/animations";
import {provideHttpClient, withInterceptors, withInterceptorsFromDi} from "@angular/common/http";
import { routes } from './app.routes';
import {authenticationInterceptor} from "./guards/auth.interceptor";

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideAnimations(),
    provideHttpClient(
      withInterceptorsFromDi(),
      withInterceptors([authenticationInterceptor])
    ),
  ]
};
