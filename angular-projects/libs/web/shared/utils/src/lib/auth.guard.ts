import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import {AuthService} from "@angular-projects/login-data-access";

export const isAuthenticatedGuard = (): CanActivateFn => {

  return () => {
    const authService = inject(AuthService);
    const router = inject(Router);
//
    if(authService.hasValidAccessToken() && authService.hasValidIdToken()){
      console.info("User logged in!");
      //authService.userProfile();
      return true;
    }

    if (router.url === "/auth/register"){
      return router.parseUrl('auth/register');
    }
    return router.parseUrl('auth/login');
  };
};
