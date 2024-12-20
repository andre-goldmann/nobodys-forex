import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NxWelcomeComponent } from './nx-welcome.component';
import {InstrumentsListComponent} from "@angular-projects/instruments-list";
import {MultipanelComponent} from "@angular-projects/multipanel";
import {MainViewComponent} from "@angular-projects/main-view";

@Component({
  imports: [RouterModule, InstrumentsListComponent, MultipanelComponent, MainViewComponent],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {

  environment = 'PROD';
  selectedInstrument = '';

  onEnvironmentChange(env: string) {
    this.environment = env;
  }

  onInstrumentSelected(instrument: string) {
    console.info('Instrument selected: ', instrument);
    this.selectedInstrument = instrument;
  }

  ngOnInit(): void {
    if (navigator.storage && navigator.storage.persist) {
      navigator.storage.persist().then((persistent) => {
        if (persistent) {
          console.log("Storage will not be cleared except by explicit user action");
        } else {
          console.log("Storage may be cleared by the UA under storage pressure.");
        }
      });
    }
  }
  title = 'forex-trades-analysis';
}
