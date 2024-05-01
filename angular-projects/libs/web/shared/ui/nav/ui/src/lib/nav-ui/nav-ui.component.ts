import {Component, inject} from '@angular/core';
import { CommonModule } from '@angular/common';
import {toSignal} from "@angular/core/rxjs-interop";
import {LayoutService} from "@angular-projects/ui-data-access-api";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {animate, keyframes, style, transition, trigger} from "@angular/animations";

@Component({
  selector: 'lib-nav-ui',
  standalone: true,
  imports: [CommonModule, RouterLinkActive, RouterLink],
  templateUrl: './nav-ui.component.html',
  styleUrl: './nav-ui.component.scss',
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
export class NavUiComponent {
  private layoutService = inject(LayoutService)
  navData = toSignal(this.layoutService.navData());

}
