import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket!: WebSocket;

  constructor() { }

  public connect(url: string): Subject<MessageEvent> {
    this.socket = new WebSocket(url);

    const observable = new Observable(observer => {
      this.socket.onmessage = observer.next.bind(observer);
      this.socket.onerror = observer.error.bind(observer);
      this.socket.onclose = () => {
        observer.complete.bind(observer);
        // Reconnect after a delay
        setTimeout(() => this.connect(url), 5000);
      };

      return this.socket.close.bind(this.socket);
    });

    const observer = {
      next: (data: Object) => {
        if (this.socket.readyState === WebSocket.OPEN) {
          this.socket.send(JSON.stringify(data));
        }
      },
    };

    return Subject.create(observer, observable);
  }
}
