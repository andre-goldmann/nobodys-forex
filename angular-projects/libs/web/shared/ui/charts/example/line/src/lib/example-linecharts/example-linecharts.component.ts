import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlotlySharedModule } from 'angular-plotly.js';

@Component({
    selector: 'lib-example-linecharts',
    imports: [CommonModule, PlotlySharedModule],
    templateUrl: './example-linecharts.component.html',
    styleUrl: './example-linecharts.component.css'
})
export class ExampleLinechartsComponent {
  trace1 = {
    x: [1, 2, 3, 4],
    y: [10, 15, 13, 17],
    mode: 'markers',
    type: 'scatter'
  };

  trace2 = {
    x: [2, 3, 4, 5],
    y: [16, 5, 11, 9],
    mode: 'lines',
    type: 'scatter'
  };

  trace3 = {
    x: [1, 2, 3, 4],
    y: [12, 9, 15, 12],
    mode: 'lines+markers',
    type: 'scatter'
  };

  public line =
    {
      data: [
        this.trace1,
        this.trace2,
        this.trace3
      ],
      layout: {width: 320, height: 480, title: 'A Fancy Plot'}
    };

  traceSpwcd = {
    y: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    mode: 'markers',
    marker: {
      size: 40,
      color: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
    }
  };

  public scatterPlotWithColorDimension = {
    data: [
      this.traceSpwcd
    ],
    layout: {width: 320, height: 480, title: 'A Fancy Plot'}
  };
}
