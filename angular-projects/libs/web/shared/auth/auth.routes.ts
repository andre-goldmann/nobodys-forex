import { Route } from '@angular/router';

export const AUTH_ROUTES: Route[] = [
  {/*wenn ich hier eine anderen Login haben will, für Client-X was muss ich tun?*/
    path: 'login',
    loadComponent: () => import('./login/ui/src/lib/login/login.component') },
  /*{
    path: 'register',
    loadComponent: () => import('./register/ui/src/lib/register/register.component'),
  },
  {
    path: 'forgot-password',
    loadComponent: () => import('./forgot-password/ui/src/lib/forgot-password/forgot-password.component'),
  },*/
  { path: 'external', redirectTo: 'https://example.com' },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  }
];
