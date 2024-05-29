import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserStoreService } from '@angular-projects/login-data-access';
import {
  StrategyEnum,
  SymbolEnum,
  Trade,
  TradesService,
  TradeStatService,
  TradeTypeEnum
} from '@angular-projects/forex-app-data-access';
import { zip } from 'rxjs';

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

  map = new Map();

  ngOnInit(): void {

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
      // sort the map so that the entries with entry > 1 come first
      this.map = new Map([...this.map.entries()].sort((a, b) => {
        const aEntry = a[1][0].entry; // Assuming 'entry' is a property of the object
        const bEntry = b[1][0].entry; // Assuming 'entry' is a property of the object

        if (aEntry > 1 && bEntry <= 1) {
          return -1; // a comes first
        }
        if (bEntry > 1 && aEntry <= 1) {
          return 1; // b comes first
        }
        return 0; // equal values, no sorting
      }));

      //console.info(this.map);
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
