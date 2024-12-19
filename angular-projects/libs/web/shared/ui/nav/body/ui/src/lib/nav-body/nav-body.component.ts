import {Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterOutlet} from "@angular/router";

@Component({
    selector: 'lib-nav-body',
    imports: [
        CommonModule,
        RouterOutlet
    ],
    templateUrl: './nav-body.component.html',
    styleUrl: './nav-body.component.scss'
})
export class NavBodyComponent {
  @Input() collapsed = false;
  @Input() screenWidth = 0;

  getBodyClass(): string {
    let styleClass = '';
    if(this.collapsed && this.screenWidth > 768) {
      styleClass = 'body-trimmed';
    } else if(this.collapsed && this.screenWidth <= 768 && this.screenWidth > 0) {
      styleClass = 'body-md-screen'
    }
    return styleClass;
  }
}
