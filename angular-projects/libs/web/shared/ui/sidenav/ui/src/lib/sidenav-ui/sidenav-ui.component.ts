import { animate, keyframes, style, transition, trigger } from '@angular/animations';
import {Component, Output, EventEmitter, OnInit, HostListener, inject, signal} from '@angular/core';
import {CommonModule} from "@angular/common";
import {RouterModule} from "@angular/router";
import {LayoutService} from "@angular-projects/ui-data-access-api";
import {AuthService} from "@angular-projects/login-data-access";
import {SideNavToggle} from "@angular-projects/sidenav-models";
import {NavbarData} from "@angular-projects/ui-data-access-models";

@Component({
  selector: 'lib-sidenav-ui',
  standalone: true,
  templateUrl: './sidenav-ui.component.html',
  styleUrl: './sidenav-ui.component.scss',
  imports: [
    CommonModule,
    RouterModule
  ],
  animations: [
    trigger('fadeInOut', [
      transition(':enter', [
        style({opacity: 0}),
        animate('350ms',
          style({opacity: 1})
        )
      ]),
      transition(':leave', [
        style({opacity: 1}),
        animate('350ms',
          style({opacity: 0})
        )
      ])
    ]),
    trigger('rotate', [
      transition(':enter', [
        animate('1000ms',
          keyframes([
            style({transform: 'rotate(0deg)', offset: '0'}),
            style({transform: 'rotate(2turn)', offset: '1'})
          ])
        )
      ])
    ])
  ]
})
export class SidenavUiComponent implements OnInit {

  private authService = inject(AuthService);
  @Output() onToggleSideNav: EventEmitter<SideNavToggle> = new EventEmitter();
  collapsed = false;
  screenWidth = 0;
  private layoutService = inject(LayoutService);
  // load this from service
  navData = signal({} as NavbarData[]);

  @HostListener('window:resize', ['$event'])
  onResize(event: any) {
    this.screenWidth = window.innerWidth;
    if(this.screenWidth <= 768 ) {
      this.collapsed = false;
      this.onToggleSideNav.emit({collapsed: this.collapsed, screenWidth: this.screenWidth});
    }
  }

  ngOnInit(): void {
    this.screenWidth = window.innerWidth;
    this.layoutService.navData().subscribe(
      {
        next: value => {
          this.navData.set(value);
        },
        error: error => {
          console.error('error receiving layout', error);
        }
      }
    )

  }

  toggleCollapse(): void {
    this.collapsed = !this.collapsed;
    this.onToggleSideNav.emit({collapsed: this.collapsed, screenWidth: this.screenWidth});
  }

  closeSidenav(): void {
    this.collapsed = false;
    this.onToggleSideNav.emit({collapsed: this.collapsed, screenWidth: this.screenWidth});
  }

  logout() {
    this.authService.logout();
  }
}

