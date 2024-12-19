import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {StringUtil} from "@angular-projects/utils";
import {CommonModule} from "@angular/common";
import { OnInit } from '@angular/core';
import {SidenavBodyComponent} from "@angular-projects/sidenav-body";
import {SidenavUiComponent} from "@angular-projects/sidenav-ui";
import {SideNavToggle} from "@angular-projects/sidenav-models";

@Component({
    imports: [CommonModule, RouterOutlet, SidenavUiComponent, SidenavBodyComponent],
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'forex-app';

  ngOnInit(): void {
    console.info(StringUtil.getIdFromUri("example:123:656"));
  }

  isSideNavCollapsed = false;
  screenWidth = 0;

  onToggleSideNav(data: SideNavToggle): void {
    this.screenWidth = data.screenWidth;
    this.isSideNavCollapsed = data.collapsed;
  }
}
