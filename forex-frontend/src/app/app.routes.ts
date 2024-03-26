import { Routes } from '@angular/router';
import {SettingsComponent} from "./components/settings/settings.component";
import {MediaComponent} from "./components/media/media.component";
import {PagesComponent} from "./components/pages/pages.component";
import {CoupensComponent} from "./components/coupens/coupens.component";
import {StatisticsComponent} from "./components/statistics/statistics.component";
import {ProductsComponent} from "./components/products/products.component";
import {DashboardComponent} from "./components/dashboard/dashboard.component";
import {isAuthenticatedGuard} from "./guards/auth.guard";

export const APP_ROUTES: Routes = [
  {
    path: 'auth',
    loadChildren: () => import('./components/auth.routes').then((m) => m.AUTH_ROUTES),
  },
  {
    path: 'dashboard',
    canActivate: [isAuthenticatedGuard()],
    component: DashboardComponent
  },
  {
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
  },
  {
    path: '',
    redirectTo: 'auth',
    pathMatch: 'full',
  }
];
