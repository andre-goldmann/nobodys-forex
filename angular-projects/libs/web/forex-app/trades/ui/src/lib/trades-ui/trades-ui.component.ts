import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Trade, TradesService } from '@angular-projects/forex-app-data-access';

@Component({
    selector: 'lib-trades-ui',
    imports: [CommonModule],
    templateUrl: './trades-ui.component.html',
    styleUrl: './trades-ui.component.css'
})
export class TradesUiComponent implements OnInit{
  prodTrades: Trade[] = [];
  selectedTrade: Trade | null = null;
  trades: Trade[] = [];

  constructor(private tradeService: TradesService) {}

  ngOnInit(): void {
    this.loadAllTrades("PROD");
  }

  loadAllTrades(env:string): void {
    this.tradeService.loadAllTrades(env).subscribe((trades) => {
      this.prodTrades = trades.slice(0, 50);
    });
  }

  selectTrade(trade: Trade): void {
    this.selectedTrade = trade;
    this.loadTrades(trade);
  }

  loadTrades(trade: Trade): void {
    this.tradeService.getTradesByProdTrade(trade).subscribe((trades) => {
      this.trades = trades;
    });
  }
}
