import { AppConfig } from '@angular-projects/app-config';
export const environment: AppConfig = {
  production: false,
  baseURL: 'http://localhost:9080/api/forex',
  clientId: 'forex_admininstrator_client',
  clientSecret: 'RdAJfqD7XCSh5P6AxnDNx2yqzQ4GNhLP',
  webHost: window.location.origin,
  keycloakHost: 'http://localhost:8080/realms/forex_admininstrator',
  requireHttps: false,
  wsURL: 'ws://localhost:9080/api/forexHandler'
};
