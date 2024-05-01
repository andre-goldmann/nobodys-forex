import { Injectable, signal } from '@angular/core';
import {UserProfile} from "@angular-projects/login-data-access";

@Injectable({
  providedIn: 'root',
})
export class UserStoreService {
  user = signal({} as UserProfile);

  setUser(user: UserProfile) {
    this.user.set(user);
  }

  public getUser(): UserProfile {
    return this.user();
  }

}
