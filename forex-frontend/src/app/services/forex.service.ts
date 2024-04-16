import {inject, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {User} from "../models/models";
import {API_GATEWAY} from "../app.config";

@Injectable({
  providedIn: 'root'
})
export class ForexService {

  private httpClient = inject(HttpClient);

  public getSymbols(){
    return this.httpClient.get<User>(API_GATEWAY + `/forex/symbols`);
  }

}
