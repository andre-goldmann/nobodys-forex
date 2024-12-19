import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';
import { Trade } from './models/trade';
import { SymbolEnum } from './models/symbol-enum';
import { StrategyEnum } from './models/strategy-enum';

export const mockProdTrades: Trade[] = [
  { id: 1, symbol: SymbolEnum.Usdjpy, strategy: StrategyEnum.VhmaWithoutReg, entry: 1.1234, exit: 1.1250, profit: 0.0016, activated: new Date(), closed: new Date(), timeframe: 'H1', type: 'BUY' },
  { id: 2, symbol: SymbolEnum.Eurusd, strategy: StrategyEnum.VhmaWithoutReg, entry: 1.2234, exit: 1.2250, profit: 0.0016, activated: new Date(), closed: new Date(), timeframe: 'H1', type: 'BUY' },
  // Add more sample data as needed
];

export const mockTrades: Trade[] = [
  { id: 3, symbol: SymbolEnum.Usdjpy, strategy: StrategyEnum.VhmaWithoutReg, entry: 1.1234, exit: 1.1250, profit: 0.0016, activated: new Date(), closed: new Date(), timeframe: 'H1', type: 'BUY' },
  { id: 4, symbol: SymbolEnum.Usdjpy, strategy: StrategyEnum.VhmaWithoutReg, entry: 1.2234, exit: 1.2250, profit: 0.0016, activated: new Date(), closed: new Date(), timeframe: 'H1', type: 'BUY' },
  // Add more sample data as needed
];

@Injectable({
  providedIn: 'root'
})
export class TradesService {
  private apiUrl: string;
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

  loadAllTrades(env:string): Observable<Trade[]> {
    return this.http.get<Trade[]>(`${this.apiUrl}/${env}`);
  }

  getTradesByProdTrade(trade: Trade): Observable<Trade[]> {
    let env = 'PROD';
    console.info(trade);
    return this.http.get<Trade[]>(`${this.apiUrl}/byid/${env}/${trade.id}`);
    //return of(mockTrades.filter(t => t.symbol === trade.symbol && t.strategy === trade.strategy));
  }

}
