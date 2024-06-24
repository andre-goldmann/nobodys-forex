import { HttpClient, HttpParams } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';
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

  getSignals(env:string): Observable<Signal[]> {
    return this.http.get<Signal[]>(  `${this.apiUrl}/${env}`);
  }

  getIgnoredSignals(): Observable<Signal[]> {
    return this.http.get<Signal[]>(  `${this.apiUrl}/ignored`);
  }

  deleteIgnoredSignal(json: string){
    let params = new HttpParams().set('json', json);
    return this.http.delete(`${this.apiUrl}/ignored/delete`, {params: params});
  }
}
