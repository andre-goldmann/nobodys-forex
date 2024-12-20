import {Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'lib-main-view',
  imports: [CommonModule],
  templateUrl: './main-view.component.html',
  styleUrl: './main-view.component.css',
})
export class MainViewComponent {
  @Input() environment = 'PROD';
  @Input() selectedInstrument = '';
}
