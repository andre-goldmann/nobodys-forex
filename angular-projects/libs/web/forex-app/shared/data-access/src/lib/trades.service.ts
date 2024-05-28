import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';
import { Trade } from './models/trade';
import { SymbolEnum } from './models/symbol-enum';
import { StrategyEnum } from './models/strategy-enum';
import { HttpUrlEncodingCodec } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class TradesService {
  private apiUrl: string;
  private codec = new HttpUrlEncodingCodec();
  constructor(private http: HttpClient,
              @Inject(APP_CONFIG) private appConfig: AppConfig) {
    this.apiUrl = `${appConfig.baseURL}/trades`;
  }

  getPositiveTrades(symbol:SymbolEnum, strategy:StrategyEnum): Observable<Trade[]> {
    return this.http.get<Trade[]>(`${this.apiUrl}/positive-profit?symbol=${symbol}&strategy=${strategy}`);
  }

  getNegativeTrades(symbol:SymbolEnum, strategy:StrategyEnum): Observable<Trade[]> {
    return this.http.get<Trade[]>( `${this.apiUrl}/negative-profit?symbol=${symbol}&strategy=${strategy}`);
  }

  updateTrade(env:string, trade: Trade): Observable<Trade> {
    const headers = new HttpHeaders({
      'X-CSRF-TOKEN': 'your-csrf-token',
      // other headers
    });
    return this.http.put<Trade>(`${this.apiUrl}/update/${env}`, trade, { headers });
  }
}
