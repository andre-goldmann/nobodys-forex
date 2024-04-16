import {Component, effect, inject, OnInit} from '@angular/core';
import { RouterModule } from '@angular/router';
import { LoginFormComponent } from './ui/login-form.component';
import { LoginService } from './data-access/login.service';
import {AuthService} from "../../services/auth.service";

@Component({
  standalone: true,
  selector: 'app-login',
  template: `
    <div class="container gradient-bg">
      @if(!authService.hasValidAccessToken()){
      <app-login-form
        [loginStatus]="loginService.status()"
      />

      } @else {
        <p>Logged in show animation here</p>
        <!--mat-spinner diameter="50" /-->
      }
    </div>
  `,
  providers: [LoginService],
  imports: [RouterModule, LoginFormComponent]
})
export default class LoginComponent {
  public loginService = inject(LoginService);
  public authService = inject(AuthService);
//  private router = inject(Router);

  constructor() {
    effect(() => {
      //if (this.authService.user()) {
        //this.router.navigate(['dashboard']);
      //}
    });
  }

}
