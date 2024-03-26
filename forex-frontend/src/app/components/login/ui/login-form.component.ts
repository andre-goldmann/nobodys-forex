import {Component, Input, inject, OnInit, signal} from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { LoginStatus } from '../data-access/login.service';
import {Router, RouterLink} from "@angular/router";
import {UsersService} from "../../../services/users.service";
import {AUTH_CONFIG, CLIENT_ID, CLIENT_SECRET, KEYCLOACK_HOST, WEB_HOST} from "../../../app.config";
import {EMPTY, filter} from "rxjs";
import {OAuthService} from "angular-oauth2-oidc";
import { JwksValidationHandler } from 'angular-oauth2-oidc-jwks';
import {AuthService} from "../../../services/auth.service";
import { MatomoTracker } from 'ngx-matomo-client';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Cookie} from "ng2-cookies";
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
  }
  ngOnInit() {
    this.authService.init();

    let i = window.location.href.indexOf('code');
    if(i != -1) {

      let code = window.location.href.substring(i + 5);
      this.retrieveToken(code);

    }
  }

  retrieveToken(code:string) {
    let params = new URLSearchParams();
    params.append('grant_type','authorization_code');
    params.append('client_id', CLIENT_ID);
    params.append('client_secret', CLIENT_SECRET);
    params.append('redirect_uri', WEB_HOST);
    params.append('code',code);

    let headers =
      new HttpHeaders({'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'});

    this._http.post(KEYCLOACK_HOST + '/protocol/openid-connect/token',
      params.toString(), { headers: headers })
      .subscribe(
        token => {
          console.log('Obtained Access token: ');
          console.info(token);
          this.saveToken(token);
        },
        err => {
          console.error(err);
          alert('Invalid Credentials');
        }
      )
  }

  saveToken(token:any) {

    var expireDate = new Date().getTime() + (100000000 * token.expires_in);
    sessionStorage.setItem("access_token", token.access_token);
    sessionStorage.setItem("refresh_token", token.refresh_token);
    sessionStorage.setItem("access_token_stored_at", "" + Date.now());
    sessionStorage.setItem("expires_at", "" + expireDate);
    this.authService.processIdToken(token);

    /*console.info("hasValidAccessToken:" + this.authService.hasValidAccessToken());
    console.info("hasValidIdToken:" + this.authService.hasValidIdToken());
    console.info("getAccessToken:" + this.authService.getAccessToken());
    console.info("getIdToken:" + this.authService.getIdToken());
    console.info("getRefreshToken:" + this.authService.getRefreshToken());*/

    window.location.href = WEB_HOST + "/dashboard";
  }

  public login(){
    this.authService.login();
  }

  public logout(){
    this.authService.logout();
  }
}
