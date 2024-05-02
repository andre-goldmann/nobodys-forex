import { AppConfig } from '@angular-projects/app-config';

export const environment: AppConfig = {
  production: false,
  baseURL: 'https://85.215.32.163:9080/api/forex',
  clientId: 'forex_admininstrator_client',
  clientSecret: 'L7YFcYYKDDpIG6dvBtISskp40O8RiyXd',
  webHost: window.location.origin,
  keycloakHost: 'https://85.215.32.163:8443/realms/forex_admininstrator',
  requireHttps: false
};
//TODO download keycloak to have no problems when offline
