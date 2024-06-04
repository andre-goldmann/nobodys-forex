import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';
import { Trade } from './models/trade';
import { HttpUrlEncodingCodec } from '@angular/common/http';
import { Signal } from './models/signal';
import { AuthService } from '@angular-projects/login-data-access';

@Injectable({
  providedIn: 'root'
})
export class SignalsService {

  private apiUrl: string;

  private codec = new HttpUrlEncodingCodec();

  constructor(private http: HttpClient,
              @Inject(APP_CONFIG) appConfig: AppConfig,
              private authService: AuthService) {
    this.apiUrl = `${appConfig.baseURL}/signals`;
  }

  getSignals(env:string): Observable<Trade[]> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'clientId': 'financialdataanalysis_admininstrator_client',
      'clientSecret': 'gnA9Dldgs3PGCaHvSMhh2eClQBhKKF8J',
      'Authorization': 'Bearer ' + this.authService.getAccessToken()  // Replace with the method to get your token
    });
    return this.http.get<Signal[]>(  `${this.apiUrl}/${env}`, { headers: headers });
  }

  getIgnoredSignals(): Observable<Trade[]> {
    return this.http.get<Signal[]>(  `${this.apiUrl}/ignored`);
  }

  deleteIgnoredSignal(json: string){
    let params = new HttpParams().set('json', json);
    return this.http.delete(`${this.apiUrl}/ignored/delete`, {params: params});
  }
}
