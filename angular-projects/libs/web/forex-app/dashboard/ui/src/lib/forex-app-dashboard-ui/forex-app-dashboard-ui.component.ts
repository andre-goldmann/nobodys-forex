import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserStoreService } from '@angular-projects/login-data-access';
import {
  StrategyEnum, SymbolEnum,
  Trade,
  TradesService,
  TradeStat,
  TradeStatService
} from '@angular-projects/forex-app-data-access';
import { flatMap, map, Observable, zip } from 'rxjs';
import { TradeTypeEnum } from '../../../../../shared/data-access/src/lib/models/trade-type-enum';


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
  //tableData: WinningTrade[] = [];
  tradeStats : TradeStat[]=[];
  prodTradeStats : TradeStat[]=[];
  selectedItem!:TradeStat;
  positiveTrades!: Trade[];
  negativeTrades!: Trade[];
  map = new Map();
  waitingTrades!: Trade[];

  ngOnInit(): void {
    /*let result = zip(this.tradeStatService.getTradeStats("dev"), this.tradeStatService.getTradeStats("prod"))
      .pipe(
        map(([dev, prod]) => {
         return [];
        })
      )*/

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

    /*this.tradeStatService.getTradeStats("dev").subscribe((data) => {
      this.tradeStats = data;
    });
    this.tradeStatService.getTradeStats("prod").subscribe((data) => {
      this.prodTradeStats = data;
    });*/
  }

  onRowClick(item: TradeStat) {
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
  }

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
