import {HttpHandlerFn, HttpInterceptorFn, HttpRequest} from '@angular/common/http';
import {inject} from "@angular/core";
import {AuthService} from "@angular-projects/login-data-access";

export const authenticationInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next:HttpHandlerFn) => {

  let authService = inject(AuthService);

  if (authService.hasValidAccessToken() && authService.hasValidIdToken()) {
    const modifiedReq = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${authService.getAccessToken()}`),
    });
    return (next(modifiedReq));
  }
  return (next(req));
};
