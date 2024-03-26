import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const isAuthenticatedGuard = (): CanActivateFn => {

  return () => {

    return true;
  };
};
