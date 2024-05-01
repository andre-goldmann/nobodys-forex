import {Inject, Injectable} from "@angular/core";
import {Observable} from "rxjs";
import {NavbarData} from "@angular-projects/ui-data-access-models";
import {APP_CONFIG, AppConfig} from "@angular-projects/app-config";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root',
})
export class LayoutService {

  constructor(
    @Inject(APP_CONFIG) private appConfig: AppConfig,
    private httpClient: HttpClient) {
  }

  navData():Observable<NavbarData[]>{
    return this.httpClient.get<NavbarData[]>(this.appConfig.baseURL + "/routes");
  }
}
