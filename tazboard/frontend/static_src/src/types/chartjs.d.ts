import { ChartData, ChartOptions } from 'chart.js'

export interface ChartMethods<T> {
  updateChart (histogramData: Array<T>): void
}
