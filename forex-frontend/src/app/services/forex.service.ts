import {inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {User} from "../models/models";
import {API_GATEWAY, SPRING_HOST} from "../app.config";

@Injectable({
  providedIn: 'root'
})
export class ForexService {

  private httpClient = inject(HttpClient)
  private forexService = inject(ForexService)

  public getSymbols(){
    return this.httpClient.get<User>(API_GATEWAY + `/forex/symbols`);
  }

}
