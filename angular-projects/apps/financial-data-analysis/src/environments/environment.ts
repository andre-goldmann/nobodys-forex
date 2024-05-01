import { AppConfig } from '@angular-projects/app-config';

export const environment: AppConfig = {
  production: false,
  baseURL: 'http://localhost:7080/api/financialdataanalysis',
  clientId: 'financialdataanalysis_admininstrator_client',
  clientSecret: 'gnA9Dldgs3PGCaHvSMhh2eClQBhKKF8J',
  webHost:window.location.origin,
  keycloakHost: 'http://localhost:8080/realms/financialdataanalysis_admininstrator',
  requireHttps: false
};
//TODO download keycloak to have no problems when offline
