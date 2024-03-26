import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import {AuthService} from "../services/auth.service";

export const isAuthenticatedGuard = (): CanActivateFn => {

  return () => {
    const authService = inject(AuthService);
    const router = inject(Router);

    //console.info("hasValidAccessToken:" + authService.hasValidAccessToken());
    //console.info("hasValidIdToken:" + authService.hasValidIdToken());
    //console.info("getAccessToken:" + authService.getAccessToken());

    if(authService.hasValidAccessToken()
      && authService.hasValidIdToken()){
      //console.info("User logged in!");
      authService.userProfile();
      return true;
    }

    console.info("User needs to login or register! Route is:" + router.url);
    if (router.url === "/auth/register"){
      return router.parseUrl('auth/register');
    }
    return router.parseUrl('auth/login');
  };
};
