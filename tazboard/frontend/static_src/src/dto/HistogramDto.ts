import { ChartData } from 'chart.js'

export class HistogramData {
  datetime!: string
  hits!: number

  static toChartdata (graphData: Array<HistogramData>, label = 'Besucher*innen gesamt'): ChartData {
    return {
      labels: graphData.map((item) => new Date(item.datetime)),
      datasets: [{
        label,
        data: graphData.map((item) => item.hits)
      }]
    }
  }
}

export class HistogramDto {
  total!: number
  data!: Array<HistogramData>
}
