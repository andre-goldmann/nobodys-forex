export interface AppConfig {
  production: boolean;
  baseURL: string;
  clientId: string;
  clientSecret: string;
  webHost:string;
  keycloakHost:string;
  requireHttps: boolean;
}
