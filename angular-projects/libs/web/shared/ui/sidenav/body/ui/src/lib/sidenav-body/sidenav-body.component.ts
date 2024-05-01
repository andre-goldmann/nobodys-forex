import {Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterOutlet} from "@angular/router";

@Component({
  selector: 'lib-sidenav-body',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  templateUrl: './sidenav-body.component.html',
  styleUrl: './sidenav-body.component.scss',
})
export class SidenavBodyComponent {
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
