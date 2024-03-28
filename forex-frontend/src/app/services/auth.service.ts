import {Injectable} from '@angular/core';

import {EMPTY, Observable} from "rxjs";
import {UserProfile} from "../models/models";
import {Credentials} from "../models/credentials";
import {Router} from "@angular/router";
import {OAuthService} from "angular-oauth2-oidc";
import {AUTH_CONFIG, CLIENT_ID, CLIENT_SECRET, WEB_HOST} from "../app.config";
import {HttpClient} from "@angular/common/http";

type LoginEventType = 'token_received';
export class LoginEvent {
  constructor(readonly type: LoginEventType) { }
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {


  constructor(private router: Router,
              private oauthService: OAuthService,
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


    this.oauthService.events
      //.pipe(filter((e) => e.type === 'token_received'))
      .subscribe((value) => {
        console.info("Event from oauthService: " + value.type);

        console.info("token_received: " + this.oauthService.getAccessToken());

        const scopes = this.oauthService.getGrantedScopes();
        console.info('scopes', scopes);
      });
    return EMPTY;
  }

  fetchToken(code:string){

    const parameters: { [key: string]: any } = {
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: WEB_HOST,
      code: code
    };

    for (const key of Object.keys(parameters)) {
      console.info(key + ": " + parameters[key]);
    }

    this.oauthService.fetchTokenUsingGrant('authorization_code', parameters)
      .then(e => {
        console.info("Got token");
        console.info(e);
      });
  }

  init() {

    this.configureCodeFlow();

    // Automatically load user profile
    this.oauthService.events
      //.pipe(filter((e) => e.type === 'token_received'))
      .subscribe((value) => {
        console.info("Event from oauthService" + value.type);
        console.info("token_received: " + this.oauthService.getAccessToken());

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
      /*this.oauthService.loadUserProfile().then(profile => {
        console.info(profile);
        let userProfile = profile as UserProfile;

        sessionStorage.setItem("user_id", userProfile.info.sid);
        this.user.set({
          id: userProfile.info.sid,
          fullName: userProfile.info.full_name,
          age: 0,
          email: userProfile.info.email,
          password: "string",
          posts: [],
          createdAt: "string",
          updatedAt: "string",
          deletedAt: "string"
        });
        console.info(this.user());

      }).catch(err => {
        console.error(err);
      });*/
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

  processIdToken(c: any) {
    //API :
    //https://github.com/manfredsteyer/angular-oauth2-oidc/blob/master/projects/lib/src/oauth-service.ts
    this.oauthService.processIdToken(c.id_token, c.access_token).then(h=>{
      this.storeIdToken(h)
    });
  }

  storeIdToken(t:any) {
      sessionStorage.setItem("id_token", t.idToken);
      sessionStorage.setItem("id_token_claims_obj", t.idTokenClaimsJson);
      sessionStorage.setItem("id_token_expires_at", "" + t.idTokenExpiresAt * 100000000);
      sessionStorage.setItem("id_token_stored_at", "" + new Date().getTime())
  }

}
