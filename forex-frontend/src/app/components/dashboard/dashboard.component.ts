import {Component, inject, signal} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {User} from "../../models/models";
import {JsonPipe} from "@angular/common";
import {UsersService} from "../../services/users.service";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.component.html',
  imports: [
    JsonPipe
  ],
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  private authService:AuthService = inject(AuthService);
  private usersService = inject(UsersService);
  user = signal({} as User);

  getUser() {
    let userId = this.authService.getUserId();
    if(userId != null) {
      this.usersService.getUserById(userId).subscribe(user => {
        console.info(`Loaded ${user}`)
        this.user.set(user);
      });
    }
  }
  saveUser(){
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
  }
}
