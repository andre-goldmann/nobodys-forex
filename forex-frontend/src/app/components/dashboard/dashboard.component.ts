import {Component, inject, OnInit, signal} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {User} from "../../models/models";
import {JsonPipe, NgForOf, NgIf} from "@angular/common";
import {UsersService} from "../../services/users.service";
import {ForexService} from "../../services/forex.service";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {BrowserModule} from "@angular/platform-browser";
import {navbarData} from "../sidenav/nav-data";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.component.html',
  imports: [
    JsonPipe,
    ReactiveFormsModule,
    NgForOf,
    NgIf
  ],
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit{

  private authService:AuthService = inject(AuthService);
  private usersService = inject(UsersService);
  private  forexService = inject(ForexService)
  user = signal({} as User);
  public symbols = signal<string[]>([]);
  getSymbols(){

    let accessToken = this.authService.getAccessToken();
    if(accessToken === null || !this.authService.hasValidAccessToken()){
      return;
    }

    //this.authService.userProfile();

  }

  getUser() {
    if(this.authService.hasValidAccessToken()) {
      /*this.usersService.getUserById(encodeURI(userId)).subscribe(user => {
        console.info(`Loaded ${user}`)
        this.user.set(user);
      });*/
      // gleicher Fehler:
      //java.lang.IllegalArgumentException: Invalid character found in method name  HTTP method names must be tokens
      this.usersService.getUsers().subscribe(user => {
        console.info(`Loaded ${user}`)
        //this.user.set(user);
      });
    }
  }
  /*saveUser(){
    let userId = this.authService.getUserId();
    if(userId != null) {
      this.usersService.saveUser({
        id: "id",
        fullName: "full_name",
        age: 0,
        email: "userProfile",
        password: "string",
        posts: [],
        createdAt: "string",
        updatedAt: "string",
        deletedAt: "string"
      }).subscribe(user => {
        console.info(`Loaded ${user}`)
        this.user.set(user);
      });
    }
  }*/
  protected readonly navData = navbarData;

  ngOnInit(): void {
    this.forexService.getSymbols().subscribe(e => {
      this.symbols.set(e);
    });
  }
}
