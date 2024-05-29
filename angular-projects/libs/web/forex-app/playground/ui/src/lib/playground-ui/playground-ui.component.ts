import { Component, computed, signal, effect } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'lib-playground-ui',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './playground-ui.component.html',
  styleUrl: './playground-ui.component.css',
})
export class PlaygroundUiComponent {
  price = 100;
  quantity = signal(1);// is writable
  total = computed( () => this.price * this.quantity()); // should not be writable

  constructor() {
    effect(() => {
      console.log('Total:', this.total());
    });
  }

  plus() {
    this.quantity.update(value => value + 1);
  }

  minus() {
    this.quantity.update(value => value - 1);
  }
}
