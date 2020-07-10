import { ChartData } from 'chart.js'

export class HistogramData {
  datetime!: string
  hits!: number
}

export class HistogramDto {
  total!: number
  data!: Array<HistogramData>

  static toChartdata (graph: HistogramDto): ChartData {
    return {
      labels: graph.data.map((item) => new Date(item.datetime).toLocaleTimeString(
        [], {
          hour: '2-digit',
          minute: '2-digit'
        }
      )),
      datasets: [{
        label: 'Number of Clicks',
        data: graph.data.map((item) => item.hits)
      }]
    }
  }
}
