import {HttpHandlerFn, HttpInterceptorFn, HttpRequest} from '@angular/common/http';
import {inject} from "@angular/core";
import {AuthService} from "../services/auth.service";

export const authenticationInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next:HttpHandlerFn) => {

  let authService = inject(AuthService);

  if (authService.hasValidAccessToken() && authService.hasValidIdToken()) {
    const modifiedReq = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${authService.getAccessToken()}`),
    });
    //console.info("########Bearer added##########");
    //console.info(req);
    return (next(modifiedReq));
  }
  console.error("########Invalid AccessToken ##########");
  return (next(req));
};
