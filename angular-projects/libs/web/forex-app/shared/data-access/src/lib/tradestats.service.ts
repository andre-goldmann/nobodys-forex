import { TradeStat } from './models/trade-stat';
import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';
import { StatsPerProdTrade } from './models/stats-per-prod-trade';

@Injectable({
  providedIn: 'root'
})
export class TradeStatService {
  private apiUrl: string;

  constructor(private http: HttpClient,
              @Inject(APP_CONFIG) private appConfig: AppConfig) {
    this.apiUrl = `${appConfig.baseURL}/trades`;
  }

  getTradeStats(env:string): Observable<TradeStat[]> {
    return this.http.get<TradeStat[]>(  `${this.apiUrl}/tradestats/${env}`);
  }

  getStatsForLastNTrades(): Observable<StatsPerProdTrade[]> {
    return this.http.get<StatsPerProdTrade[]>(`${this.apiUrl}/statsforlastntrades`);
  }

}
