import {Component, OnInit} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {StringUtil} from '@angular-projects/utils'
import {CommonModule} from "@angular/common";
import {SidenavUiComponent} from "@angular-projects/sidenav-ui";
import {SidenavBodyComponent} from "@angular-projects/sidenav-body";
import {NavBodyComponent} from "@angular-projects/nav-body";
import {NavUiComponent} from "@angular-projects/nav-ui";
import {SideNavToggle} from "@angular-projects/sidenav-models";



@Component({
  standalone: true,
  selector: 'app-root',
  //imports: [CommonModule, RouterOutlet, NavBodyComponent, NavUiComponent],
  imports: [CommonModule, RouterOutlet, SidenavUiComponent, SidenavBodyComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  title = 'financial-data-analysis';

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
