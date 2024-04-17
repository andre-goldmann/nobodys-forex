import {inject, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {User} from "../models/models";
import {API_GATEWAY} from "../app.config";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ForexService {

  private httpClient = inject(HttpClient);

  public getSymbols():Observable<string[]>{
    return this.httpClient.get<string[]>(API_GATEWAY + `/forex/symbols`);
  }

}
