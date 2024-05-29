import { Component, inject, Inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subject } from 'rxjs';
import { APP_CONFIG, AppConfig } from '@angular-projects/app-config';
import { Signal, SignalsService, WebsocketService } from '@angular-projects/forex-app-data-access';

@Component({
  selector: 'lib-signals-ui',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './signals-ui.component.html',
  styleUrl: './signals-ui.component.css',
})
export class SignalsUiComponent implements OnInit {

  protected signalsService:SignalsService = inject(SignalsService);
  signals = signal<Signal[]>([]);
  ignoredSignals = signal<Signal[]>([]);
  private socket!: Subject<MessageEvent>;

  private websocketService: WebsocketService = inject(WebsocketService);

  constructor(@Inject(APP_CONFIG) private appConfig: AppConfig) {
  }

  ngOnInit(): void {

    this.socket = this.websocketService.connect(`${this.appConfig.wsURL}`);

    this.socket.subscribe(
      message =>
      {
        console.log('Received message: ', message.data);
        let newSignal = JSON.parse(message.data);
        this.signals.update(values => {
          return [newSignal, ...values];
        });
      },
      error => console.error('Error: ', error),
      () => console.log('WebSocket connection closed')
    );

    this.signalsService.getSignals('prod').subscribe((data) => {
      this.signals.set(data);
    });
    this.signalsService.getIgnoredSignals().subscribe((data) => {
      this.ignoredSignals.set(data);
    });
  }

  deleteIgnoredSignals(json: string) {
    this.signalsService.deleteIgnoredSignal(json).subscribe(  {
      next: () => {
        console.info("Deleted signal!");
      },
      error: (error) => {
        console.error('Error: ', error);
      }
    });
  }
}
