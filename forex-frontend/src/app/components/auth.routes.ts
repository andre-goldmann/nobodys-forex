import { Route } from '@angular/router';

export const AUTH_ROUTES: Route[] = [
  {/*wenn ich hier eine anderen Login haben will, für Client-X was muss ich tun?*/
    path: 'login',
    loadComponent: () => import('./login/login.component') },
  {
    path: 'register',
    loadComponent: () => import('./register/register.component'),
  },
  {
    path: 'forgot-password',
    loadComponent: () => import('./forgot-password/forgot-password.component'),
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  },
];
