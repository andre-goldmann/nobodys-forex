import {Component, inject, OnInit, signal} from '@angular/core';
import {Router, RouterModule} from "@angular/router";
import { AuthService, UserProfile, UserStoreService } from '@angular-projects/login-data-access';
import {SpinnerComponent} from "@angular-projects/spinner-component";
import {AsyncPipe, CommonModule} from "@angular/common";
import {BehaviorSubject} from "rxjs";


@Component({
  standalone: true,
  selector: 'lib-login',
  template: `
    <div class="container gradient-bg">
      @if(!authService.hasValidAccessToken()){
      } @else {
        <lib-spinner-component class="ml-4" *ngIf="isLoading$ | async"></lib-spinner-component>
      }
    </div>
  `,
  imports: [CommonModule, RouterModule, SpinnerComponent, AsyncPipe]
})
export default class LoginComponent implements OnInit{
  private isLoadingSubject = new BehaviorSubject<boolean>(false);
  isLoading$ = this.isLoadingSubject.asObservable();

  private userStoreService:UserStoreService = inject(UserStoreService);
  public authService = inject(AuthService);
  private router = inject(Router);

  ngOnInit(): void {

    this.authService.init();

    // Always try this???
    let i = window.location.href.indexOf('code');
    if(i != -1) {
      let code = window.location.href.substring(i + 5);
      this.isLoadingSubject.next(true);

      this.authService.fetchToken(code).then(e => {
        console.info("Got token...");
        this.isLoadingSubject.next(false);
        this.authService.userProfile().then(profile => {
          console.info(profile);
          let userProfile = profile as UserProfile;
          this.userStoreService.setUser(userProfile);
        });
        this.router.navigate(["/dashboard"]);
      });
    }
    else {
      if (
        !this.authService.hasValidAccessToken() && !this.authService.hasValidIdToken()) {
        sessionStorage.clear();
        this.authService.login();
      } else {
        // immer dashboard??
        this.router.navigate(['dashboard']);
      }
    }
  }

}
