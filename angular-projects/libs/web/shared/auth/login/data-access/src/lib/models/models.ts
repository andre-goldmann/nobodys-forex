export interface Models {
  email: string;
  password: string;
}

export type LoginStatus = 'pending' | 'authenticating' | 'success' | 'error' | 'logout';

export interface LoginState {
  status: LoginStatus;
}

export interface UserProfile {
  info: {
    exp: number;
    iat: number;
    auth_time: number;
    jti: string;
    iss: string;
    aud: string;
    sub: string;
    typ: string;
    azp: string;
    nonce: string;
    session_state: string;
    at_hash: string;
    acr: string;
    sid: string;
    email_verified: boolean;
    preferred_username: string;
    email: string;
  }
}
