import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'forex-frontend';
  constructor(private http:HttpClient) {
    this.http.get("http://localhost:8080/trades").subscribe(e => {
      console.info(e);
    });
  }
}
