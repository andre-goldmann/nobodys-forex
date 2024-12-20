import {Component, EventEmitter, Output} from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'lib-instruments-list',
  imports: [CommonModule],
  templateUrl: './instruments-list.component.html',
  styleUrl: './instruments-list.component.css',
})
export class InstrumentsListComponent {
  @Output() instrumentSelected = new EventEmitter<string>();
  instruments = ['EURUSD', 'GBPUSD', 'USDCAD'];
// Mock data for price direction and prices; replace with actual data logic
  instrumentData: { [key: string]: { direction: string, price: number } } = {
    'EURUSD': { direction: 'up', price: 1.1234 },
    'GBPUSD': { direction: 'down', price: 1.3456 },
    'USDCAD': { direction: 'up', price: 1.2345 }
  };


  onInstrumentClick(instrument: string) {
    this.instrumentSelected.emit(instrument);
  }

  clearSelection() {
    this.instrumentSelected.emit('');
  }

  getFlagUrl(countryCode: string): string {
    const countryMap: { [key: string]: string } = {
      'E': 'EU',
      'G': 'GB',
      'U': 'US',
      'C': 'CA'
    };
    return `https://s3-symbol-logo.tradingview.com/country/${countryMap[countryCode]}.svg`;
  }

  getPriceDirectionClass(instrument: string): string {
    return this.instrumentData[instrument].direction === 'up' ? 'up-arrow' : 'down-arrow';
  }

  getPriceDirectionSymbol(instrument: string): string {
    return this.instrumentData[instrument].direction === 'up' ? '▲' : '▼';
  }

  getInstrumentPrice(instrument: string): string {
    return this.instrumentData[instrument].price.toFixed(4);
  }
}
