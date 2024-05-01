import { Route } from '@angular/router';
import {isAuthenticatedGuard} from "@angular-projects/utils";
import {ForexAppDashboardUiComponent} from "@angular-projects/forex-app-dashboard-ui";
import {LogoutComponent} from "./LogoutComponent";

export const APP_ROUTES: Route[] = [
  {
    path: 'auth',
    loadChildren: () => import('@angular-projects/auth_routes').then((m) => m.AUTH_ROUTES),
  },
  {
    path: 'dashboard',
    canActivate: [isAuthenticatedGuard()],
    component: ForexAppDashboardUiComponent
  },
  {
    path: 'logout',
    component: LogoutComponent
  },
  { path: 'external', redirectTo: 'https://example.com' },
  /*{
    path: 'products',
    canActivate: [isAuthenticatedGuard()],
    component: ProductsComponent},
  {
    path: 'statistics',
    canActivate: [isAuthenticatedGuard()],
    component: StatisticsComponent
  },
  {
    path: 'coupens',
    canActivate: [isAuthenticatedGuard()],
    component: CoupensComponent
  },
  {
    path: 'pages',
    canActivate: [isAuthenticatedGuard()],
    component: PagesComponent
  },
  {
    path: 'media',
    canActivate: [isAuthenticatedGuard()],
    component: MediaComponent
  },
  {
    path: 'settings',
    canActivate: [isAuthenticatedGuard()],
    component: SettingsComponent
  },*/
  {
    path: '',
    redirectTo: 'auth',
    pathMatch: 'full',
  }
];
