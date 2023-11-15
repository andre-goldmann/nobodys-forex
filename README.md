https://tvsignals.nobodys-forex.duckdns.org/

https://nobodys-forex.duckdns.org/

https://www.duckdns.org/domains


Checks:

https://backend.nobodys-forex.duckdns.org/linesinfo/?symbol=EURUSD&timeframe=PERIOD_H4

https://tvsignals.nobodys-forex.duckdns.org/

curl -H 'Content-Type: application/json; charset=utf-8' -d '{"symbol": "BTCUSD", "timestamp": "11.03.2023", "type":"buy", "entry": 1.0, "sl": 1.1, "tp": 1.2, "strategy": "Hello World"}' -X POST https://tvsignals.nobodys-forex.duckdns.org/signal

curl -H 'Content-Type: application/json; charset=utf-8' -d '{"symbol": "BTCUSD", "timestamp": "11.03.2023", "type":"buy", "entry": 1.0, "sl": 1.1, "tp": 1.2, "strategy": "Hello World"}' -X POST http://85.215.32.163/signal

                                                            {"symbol": "BTCUSD", "timestamp": "11.03.2023", "type":"buy", "entry": 1.0,     "sl": 1.1, "tp": 1.2, "strategy": "HalfTrend"}
                                                            {"symbol": "BTCUSD", "timestamp": "11.03.2023", "type":"sell","entry":27498.22, "sl":27390,"tp":400, "strategy":"TestIndicator"}
                                                            {"symbol": "GBPUSD", "timestamp": "11.03.2023", "type":"buy", "entry": 1.0, "sl": 1.1, "tp": 1.2, "strategy": "HalfTrend"}        


docker compose up --build
If you want to stop the containers, type: "docker-compose down"
If you want to remove the containers, type: "docker-compose down -v" after this command finished, type: "docker-compose down --rmi all"

URLS:
http://85.215.32.163:6081/linesinfo/?symbol=XRPUSD&timeframe=PERIOD_D1
http://85.215.32.163:6081/linesinfo/?symbol=XRPUSD&timeframe=PERIOD_M15
http://85.215.32.163:6081/lastCandle/?symbol=AUDUSD&timeFrame=PERIOD_D1