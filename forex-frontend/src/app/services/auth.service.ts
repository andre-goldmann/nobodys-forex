import {Injectable, signal} from '@angular/core';

import {EMPTY, filter, Observable} from "rxjs";
import {Post, User, UserProfile} from "../models/models";
import {Credentials} from "../models/credentials";
import {Router} from "@angular/router";
import {OAuthService} from "angular-oauth2-oidc";
import {AUTH_CONFIG, CLIENT_ID, CLIENT_SECRET, KEYCLOACK_HOST, WEB_HOST} from "../app.config";
import {JwksValidationHandler} from "angular-oauth2-oidc-jwks";
import {HttpClient, HttpHeaders} from "@angular/common/http";

type LoginEventType = 'token_received';
export class LoginEvent {
  constructor(readonly type: LoginEventType) { }
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  //user = signal({} as User);

  constructor(private router: Router,
              private oauthService: OAuthService,
              private http:HttpClient) {
  }

  //public getUser():User{
  //return this.user();
  //}

  createAccount(credentials: Credentials):Observable<void> {
    return EMPTY;
  }

  login() {
    console.info("Start login...");

    this.oauthService.loadDiscoveryDocumentAndLogin()
      .then(() => {
        console.info("then loadDiscoveryDocumentAndLogin executed");
        this.oauthService.setupAutomaticSilentRefresh();

        //this.initialized$.next(void 0);
        //this.initialized$.complete();
      }, () => {
        console.info("loadDiscoveryDocumentAndLogin executed");
        //this.initialized$.next();
        ////this.initialized$.complete();
      });

    this.oauthService.discoveryDocumentLoaded$.subscribe(e =>{
      console.info(e);
    });


    this.oauthService.events
      //.pipe(filter((e) => e.type === 'token_received'))
      .subscribe((value) => {
        console.info("Event from oauthService: " + value.type);

        console.info("token_received: " + this.oauthService.getAccessToken());
        /*this.oauthService.loadUserProfile().then(profile => {
          console.info(profile);
        });*/

        const scopes = this.oauthService.getGrantedScopes();
        console.info('scopes', scopes);
      });
    return EMPTY;
  }

  fetchToken(code:string){
    console.info("I am using:")
    console.info(KEYCLOACK_HOST + '/protocol/openid-connect/token');
    console.info("Impl uses:");
    console.info(this.oauthService.tokenEndpoint);

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
    console.info(this.oauthService.getAccessToken());
    console.info("state: " + this.oauthService.state);
    console.info("scope: " + this.oauthService.scope);
    this.configureCodeFlow();

    console.info("using-flow: " + sessionStorage.getItem('flow'));
    console.info("redirectUri: " + this.oauthService.redirectUri);
    console.info("logoutUrl: " + this.oauthService.logoutUrl);

    // Automatically load user profile
    this.oauthService.events
      //.pipe(filter((e) => e.type === 'token_received'))
      .subscribe((value) => {
        console.info("Event from oauthService" + value.type);
        console.info("token_received: " + this.oauthService.getAccessToken());
        /*this.oauthService.loadUserProfile().then(profile => {
          console.info(profile);
        });*/

        const scopes = this.oauthService.getGrantedScopes();
        console.info('scopes', scopes);
      });
  }

  private configureCodeFlow() {

    this.oauthService.configure(AUTH_CONFIG);

    //this.oauthService.tokenValidationHandler = new JwksValidationHandler();
    /*this.oauthService.loadDiscoveryDocumentAndTryLogin()
    // das führt nach Start der Seite gleich zum Login
    //this.oauthService.loadDiscoveryDocumentAndLogin()
      .then(() => {
        this.oauthService.setupAutomaticSilentRefresh();
        //this.initialized$.next(void 0);
        //this.initialized$.complete();
      }, () => {
        //this.initialized$.next();
        ////this.initialized$.complete();
      });*/
  }

  private configureImplicitFlow() {
    this.oauthService.configure(AUTH_CONFIG);
    //this.oauthService.tokenValidationHandler = new JwksValidationHandler();

    this.oauthService.loadDiscoveryDocumentAndTryLogin().then((_) => {
      //if (useHash) {
        //  this.router.navigate(['/']);
      //}
    });

    // Optional
    // this.oauthService.setupAutomaticSilentRefresh();

    // Display all events
    /*this.oauthService.events.subscribe((e) => {
      // tslint:disable-next-line:no-console
      console.info('oauth/oidc event', e);
    });

    this.oauthService.events
      .pipe(filter((e) => e.type === 'session_terminated'))
      .subscribe((e) => {
        // tslint:disable-next-line:no-console
        console.info('Your session has been terminated!');
      });*/
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
