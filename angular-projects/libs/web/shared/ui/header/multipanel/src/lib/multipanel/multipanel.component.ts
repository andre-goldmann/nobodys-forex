import {Component, EventEmitter, Output} from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'lib-multipanel',
  imports: [CommonModule, FormsModule],
  templateUrl: './multipanel.component.html',
  styleUrl: './multipanel.component.css',
})
export class MultipanelComponent {
  @Output() environmentChange = new EventEmitter<string>();
  selectedEnvironment = 'PROD';

  onEnvironmentChange() {
    this.environmentChange.emit(this.selectedEnvironment);
  }
}
