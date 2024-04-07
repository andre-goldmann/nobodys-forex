import {inject, Injectable} from '@angular/core';

import {EMPTY, Observable} from "rxjs";
import {UserProfile} from "../models/models";
import {Credentials} from "../models/credentials";
import {Router} from "@angular/router";
import {OAuthService} from "angular-oauth2-oidc";
import {AUTH_CONFIG, CLIENT_ID, CLIENT_SECRET, WEB_HOST} from "../app.config";
import {HttpClient} from "@angular/common/http";


@Injectable({
  providedIn: 'root',
})
export class AuthService {

  private router:Router = inject(Router);

  constructor(private oauthService: OAuthService,
              private http:HttpClient) {
  }


  createAccount(credentials: Credentials):Observable<void> {
    return EMPTY;
  }

  login() {
    console.info("Start login...");

    this.oauthService.loadDiscoveryDocumentAndLogin()
      .then(() => {
        console.info("then loadDiscoveryDocumentAndLogin executed");
        this.oauthService.setupAutomaticSilentRefresh();

      }, () => {
        console.info("loadDiscoveryDocumentAndLogin executed");

      });

    this.oauthService.discoveryDocumentLoaded$.subscribe(e =>{
      console.info(e);
    });


    /*this.oauthService.events
      //.pipe(filter((e) => e.type === 'token_received'))
      .subscribe((value) => {
        console.info("Event from oauthService: " + value.type);

        console.info("token_received: " + this.oauthService.getAccessToken());

        const scopes = this.oauthService.getGrantedScopes();
        console.info('scopes', scopes);
      });*/
    return EMPTY;
  }

  fetchToken(code:string){

    const parameters: { [key: string]: any } = {
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: WEB_HOST,
      code: code
    };

    this.oauthService.fetchTokenUsingGrant('authorization_code', parameters)
      .then(e => {
        console.info("Got token...");
        this.router.navigate(["/dashboard"]);
      });
  }

  init() {

    this.configureCodeFlow();

    // Automatically load user profile
    this.oauthService.events
      //.pipe(filter((e) => e.type === 'token_received'))
      .subscribe((value) => {
        console.info("Event from oauthService" + value.type);

        const scopes = this.oauthService.getGrantedScopes();
        console.info('scopes', scopes);
      });
  }

  private configureCodeFlow() {
    this.oauthService.configure(AUTH_CONFIG);
  }


  logout() {
    this.oauthService.logOut();
    sessionStorage.removeItem("user_id");
  }

  getUserId(){
    return sessionStorage.getItem("user_id");
  }

  userProfile(){
    //maybe store this to localstorage
    //console.info(sessionStorage.getItem("user_id"));
    if(sessionStorage.getItem("user_id") === null) {
      if(AUTH_CONFIG.userinfoEndpoint) {
        console.info("Loading user profile from " + AUTH_CONFIG.userinfoEndpoint);
        this.http.get(AUTH_CONFIG.userinfoEndpoint).subscribe(profile => {
          let userProfile = profile as UserProfile;
          console.info(profile);
          sessionStorage.setItem("user_id", userProfile.sub);
        });
      }
    }
  }

  hasValidAccessToken() {
    return this.oauthService.hasValidIdToken();
  }

  hasValidIdToken() {
    return this.oauthService.hasValidIdToken();
  }

  getAccessToken() {
    return this.oauthService.hasValidAccessToken() ? this.oauthService.getAccessToken() : null;
  }

}
