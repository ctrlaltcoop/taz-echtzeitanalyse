import { ChartData, ChartOptions } from 'chart.js'

export interface VueChartMethods {
  renderChart(data: ChartData, options?: ChartOptions): void;
}
