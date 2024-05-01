import { Routes } from '@angular/router';
import {FdaDashboardUiComponent} from "@angular-projects/fda-dashboard-ui";
import {isAuthenticatedGuard} from "@angular-projects/utils";

export const APP_ROUTES: Routes = [
  {
    path: 'auth',
    loadChildren: () => import('@angular-projects/auth_routes').then((m) => m.AUTH_ROUTES),
  },
  {
    path: 'dashboard',
    canActivate: [isAuthenticatedGuard()],
    component: FdaDashboardUiComponent
  },
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
