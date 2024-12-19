import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';
import {SvgIconComponent} from '@ngneat/svg-icon';

@Component({
    selector: 'lib-spinner-component',
    imports: [CommonModule, SvgIconComponent],
    templateUrl: './spinner-component.component.html',
    styleUrl: './spinner-component.component.scss',
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class SpinnerComponent {
  @Input() size = "xl";
}
