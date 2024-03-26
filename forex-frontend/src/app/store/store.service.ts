import { Injectable, signal } from '@angular/core';
import { User } from '../models/models';

@Injectable({
  providedIn: 'root',
})
export class StoreService {
  user = signal({} as User);
  token = signal('');
  setUser(user: User) {
    this.user.set(user);
  }
  setToken(token: string) {
    this.token.set(token);
  }

  public getUser(): User {
    return this.user();
  }

  authToken(): string {
    return this.token();
  }
}
