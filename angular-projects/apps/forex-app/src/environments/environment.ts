import { AppConfig } from '@angular-projects/app-config';

export const environment: AppConfig = {
  production: false,
  baseURL: 'http://localhost:7080/api/forex',
  clientId: 'forex_admininstrator_client',
  clientSecret: 'fPeHnS3SUWvOH4I8lzHfym7Aq1fSSEIq',
  webHost: window.location.origin,
  keycloakHost: 'http://localhost:8080/realms/forex_admininstrator',
  requireHttps: false
};
//TODO download keycloak to have no problems when offline
