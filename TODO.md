- verarbeitung von noch mehr Signalen -> Broker finden
- wenn Signal auf H4 dann größere SL und TP
- bessere Auswertung der Trades (Dev-Prod): Prod-Trade mit aktuellem Dev- als Prod-Ergebnissen see trading_db_public_ProdTrades.ods
- bessere Darstellung der Ignored-Signals
- Aktulalisierung der Prod-Trade-History
- TODO check that TrendInfo is up to date
- Autoimport forex-domain within api-gateway, forex-backend-java and angular-projects
- ADD PK of Trades to ProdTrades -> select * from "Trades" where symbol='EURUSD' and sl=1.074252671661376 and tp=1.064387328338624 and strategy='Super AI Trend_WITHOUT_REG';
- Collect data from winning trades:
  - EMA, SMA 20,50,100,200
  - RSI 14
  - MACD 12,26,9
  - Stoch 14,3,3
  - ADX 14
  - CCI 14
  - ATR 14
  - Bollinger Bands 20
  - Ichimoku
  - Parabolic SAR
  - Pivot Points
  - Fibonacci Retracements
- show last stored Candles