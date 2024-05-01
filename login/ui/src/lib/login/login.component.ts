import {Component, inject, Input, OnInit} from '@angular/core';
import {ReactiveFormsModule} from "@angular/forms";
import {AuthService, LoginStatus} from "@angular-projects/auth-data-access";
import {HttpClient} from "@angular/common/http";
import {RouterLink} from "@angular/router";

@Component({
  selector: 'lib-login',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent implements OnInit {
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
