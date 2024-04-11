import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../models/models';
import { StoreService } from '../store/store.service';
import {SPRING_HOST} from "../app.config";

@Injectable({
  providedIn: 'root',
})
export class UsersService {

  constructor(
    private httpClient: HttpClient,
    private storeService: StoreService) {}

  public getUserById(id:string): Observable<User> {
    return this.httpClient.get<User>(SPRING_HOST + `/api/users/${id}`);
  }

  public saveUser(user:User): Observable<User> {
    return this.httpClient.post<User>(SPRING_HOST + `/api/users`, user);
  }

  public getUsers(): Observable<User[]> {
    return this.httpClient.get<User[]>(SPRING_HOST + '/api/users');
  }

  updateUser(user: any): Observable<User> {
    return this.httpClient.put<User>(SPRING_HOST + '/api/users', user);
  }
}
