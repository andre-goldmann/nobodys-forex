import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlotlyModule } from 'angular-plotly.js';

@Component({
    selector: 'lib-example-barcharts',
    imports: [CommonModule, PlotlyModule],
    templateUrl: './example-barcharts.component.html',
    styleUrl: './example-barcharts.component.css'
})
export class ExampleBarchartsComponent {
  public graph = {
    data: [
      { x: [1, 2, 3], y: [2, 6, 3], type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
      { x: [1, 2, 3], y: [2, 5, 3], type: 'bar' },
    ],
    layout: {width: 320, height: 240, title: 'A Fancy Plot'}
  };

  public bar = {
    data: [
      {
        x: ['giraffes', 'orangutans', 'monkeys'],
        y: [20, 14, 23],
        type: 'bar'
      }
    ],
    layout: {width: 320, height: 240, title: 'A Fancy Plot'}
  };

  trace1 = {
    x: ['giraffes', 'orangutans', 'monkeys'],
    y: [20, 14, 23],
    name: 'SF Zoo',
    type: 'bar'
  };

  trace2 = {
    x: ['giraffes', 'orangutans', 'monkeys'],
    y: [12, 18, 29],
    name: 'LA Zoo',
    type: 'bar'
  };
  public groupedBarChart =
    {
      data: [
        this.trace1,
        this.trace2
      ],
      layout: {width: 320, height: 240, title: 'A Fancy Plot', barmode: 'group'}
    };
}
