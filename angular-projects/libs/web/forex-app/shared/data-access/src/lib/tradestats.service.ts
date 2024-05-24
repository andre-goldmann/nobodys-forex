import { TradeStat } from './models/trade-stat';
import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';

@Injectable({
  providedIn: 'root'
})
export class TradeStatService {
  private apiUrl: string;

  constructor(private http: HttpClient,
              @Inject(APP_CONFIG) private appConfig: AppConfig) {
    this.apiUrl = `${appConfig.baseURL}/tradestats`;
  }

  getTradeStats(env:string): Observable<TradeStat[]> {
    return this.http.get<TradeStat[]>(  `${this.apiUrl}/${env}`);
  }

}
