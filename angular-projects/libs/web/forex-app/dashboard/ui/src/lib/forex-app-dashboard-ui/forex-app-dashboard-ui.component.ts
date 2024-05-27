import { Component, Inject, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserStoreService } from '@angular-projects/login-data-access';
import {
  StrategyEnum, SymbolEnum,
  Trade,
  TradesService,
  TradeStat,
  TradeStatService, WebsocketService
} from '@angular-projects/forex-app-data-access';
import { Subject, zip } from 'rxjs';
import { TradeTypeEnum } from '../../../../../shared/data-access/src/lib/models/trade-type-enum';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';
import { Signal } from '../../../../../shared/data-access/src/lib/models/signal';


@Component({
  selector: 'lib-forex-app-dashboard-ui',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './forex-app-dashboard-ui.component.html',
  styleUrl: './forex-app-dashboard-ui.component.scss',
})
export class ForexAppDashboardUiComponent implements OnInit{
  // inject TradesService
  protected tradeService:TradesService = inject(TradesService);

  protected tradeStatService:TradeStatService = inject(TradeStatService);

  protected userStoreService:UserStoreService = inject(UserStoreService);
  /*tableData: WinningTrade[] = [];
  tradeStats : TradeStat[]=[];
  prodTradeStats : TradeStat[]=[];
  selectedItem!:TradeStat;
  positiveTrades!: Trade[];
  negativeTrades!: Trade[];*/
  map = new Map();
  waitingTrades!: Trade[];
  private socket!: Subject<MessageEvent>;
  private websocketService: WebsocketService = inject(WebsocketService);

  constructor(@Inject(APP_CONFIG) private appConfig: AppConfig) {
  }

  signals = signal<Signal[]>([]);

  ngOnInit(): void {

    this.socket = this.websocketService.connect(`${this.appConfig.wsURL}`);

    this.socket.subscribe(
      message =>
      {
        console.log('Received message: ', message.data);
        let newSignal = JSON.parse(message.data);
        this.signals.update(values => {
          return [...values, newSignal];
        });
      },
      error => console.error('Error: ', error),
      () => console.log('WebSocket connection closed')
    );

    /*let result = zip(this.tradeStatService.getTradeStats("dev"), this.tradeStatService.getTradeStats("prod"))
      .pipe(
        map(([dev, prod]) => {
         return [];
        })
      )*/
    // TODO hier ist schon wieder viel zu viel logic drin, das sollte in den Service ausgelagert werden
    zip(this.tradeStatService.getTradeStats("dev"), this.tradeStatService.getTradeStats("prod")).
      subscribe(d => {
        let devData = d[0];
        let prodData = d[1];
        // TODO eigentlich sollte das auch anders funktionieren, also ohne Verwendung der Map
        devData.forEach(entry => {
          let prodEntries = prodData.filter((stat) => stat.symbol == entry.symbol && stat.strategy == entry.strategy);
          if (prodEntries.length > 0){
            //console.info("Prod-Stat found:" + prodEntries);
            this.map.set(entry.symbol + "-" + entry.strategy, [entry, prodEntries[0]])
          } else {
            this.map.set(entry.symbol + "-" + entry.strategy, [entry])
          }
        });
      //console.info(this.map);
    });
    this.tradeService.getWaitingTrades('prod').subscribe((data) => {
      this.waitingTrades = data;
    });

  }

  /*onRowClick(item: TradeStat) {
    //console.info(item);
    //console.info("Loading trade-details");
    this.selectedItem = item;
    this.positiveTrades = [];
    this.negativeTrades = [];
    this.tradeService.getPositiveTrades(item.symbol, item.strategy).subscribe((data) => {
      //console.info("Positive-Data: " + data);
      this.positiveTrades = data;
    });

    this.tradeService.getNegativeTrades(item.symbol, item.strategy).subscribe((data) => {
      //console.info("Negative-Data: " + data);
      this.negativeTrades = data;
    });
  }*/

  updateTrade() {
    let exampleTrade: Trade = {
      id: 1,
      type: TradeTypeEnum.Buy,
      symbol: SymbolEnum.Usdjpy,
      strategy: StrategyEnum.VhmaWithoutReg,
      activated: new Date(),
      closed: new Date(),
      entry: 1.1234,
      exit: 1.1250,
      profit: 0.0016
    };
    this.tradeService.updateTrade("prod", exampleTrade)
      .subscribe(value => {
        console.info("Trade updated: " + value);
      });
  }
}
