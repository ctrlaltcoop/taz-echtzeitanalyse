import { ChartData } from 'chart.js'

export class HistogramData {
  datetime!: string
  hits!: number

  static toChartdata (graphData: Array<HistogramData>): ChartData {
    return {
      labels: graphData.map((item) => new Date(item.datetime).toLocaleTimeString(
        [], {
          hour: '2-digit',
          minute: '2-digit'
        }
      )),
      datasets: [{
        label: 'Number of Clicks',
        data: graphData.map((item) => item.hits)
      }]
    }
  }
}

export class HistogramDto {
  total!: number
  data!: Array<HistogramData>
}
