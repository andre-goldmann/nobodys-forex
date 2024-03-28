import {Component, Input, inject, OnInit} from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { LoginStatus } from '../data-access/login.service';
import {Router, RouterLink} from "@angular/router";
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

  private router:Router = inject(Router);
  private authService = inject(AuthService);
  keycloakUrl: string = KEYCLOACK_HOST;
  keycloakSecret: string = CLIENT_SECRET;
  keycloakClient: string = CLIENT_ID;
  redirectUr: string = WEB_HOST;

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
