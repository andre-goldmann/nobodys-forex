import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';
import { Trade } from './models/trade';
import { HttpUrlEncodingCodec } from '@angular/common/http';
import { Signal } from './models/signal';

@Injectable({
  providedIn: 'root'
})
export class SignalsService {

  private apiUrl: string;

  private codec = new HttpUrlEncodingCodec();

  constructor(private http: HttpClient,
              @Inject(APP_CONFIG) private appConfig: AppConfig) {
    this.apiUrl = `${appConfig.baseURL}/signals`;
  }

  getSignals(env:string): Observable<Trade[]> {
    return this.http.get<Signal[]>(  `${this.apiUrl}/${env}`);
  }

  getIgnoredSignals(): Observable<Trade[]> {
    return this.http.get<Signal[]>(  `${this.apiUrl}/ignored`);
  }
}
