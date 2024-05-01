import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormControl} from "@angular/forms";
import {InputComponent} from "@angular-projects/input-component";
import {of} from "rxjs";
import {SpinnerComponent} from "@angular-projects/spinner-component";

@Component({
  selector: 'lib-fda-dashboard-ui',
  standalone: true,
  imports: [CommonModule, InputComponent, SpinnerComponent],
  templateUrl: './fda-dashboard-ui.component.html',
  styleUrl: './fda-dashboard-ui.component.scss',
})
export class FdaDashboardUiComponent {
  searchControl: FormControl = new FormControl('');
  isLoading$ = of();
  //
}
