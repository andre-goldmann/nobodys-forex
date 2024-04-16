import {Component, Input, inject, OnInit} from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { LoginStatus } from '../data-access/login.service';
import {RouterLink} from "@angular/router";
import {CLIENT_ID, CLIENT_SECRET, KEYCLOACK_HOST, WEB_HOST} from "../../../app.config";
import {AuthService} from "../../../services/auth.service";
import {HttpClient} from "@angular/common/http";

@Component({
  standalone: true,
  selector: 'app-login-form',
  imports: [
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginFormComponent implements OnInit {
  @Input({ required: true }) loginStatus!: LoginStatus;

  private authService = inject(AuthService);

  constructor(private _http:HttpClient) {
    console.info("LoginFormComponent constructor called!!");
  }
  ngOnInit() {
    this.authService.init();

    let i = window.location.href.indexOf('code');
    if(i != -1) {
      let code = window.location.href.substring(i + 5);
      this.authService.fetchToken(code);
    }
  }

  public login(){
    this.authService.login();
  }

  public logout(){
    this.authService.logout();
  }
}
