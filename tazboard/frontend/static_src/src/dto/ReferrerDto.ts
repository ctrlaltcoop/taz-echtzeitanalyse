import { ChartData } from 'chart.js'

export class ReferrerData {
  referrerclass!: string
  value!: number
}

export class ReferrerDto {
  total!: number
  data!: Array<ReferrerData>

  static toChartdata (graph: ReferrerDto): ChartData {
    return {
      labels: graph.data.map((item) => new Date(item.referrerclass).toLocaleTimeString(
        [], {
          hour: '2-digit',
          minute: '2-digit'
        }
      )),
      datasets: [{
        label: 'Number of Clicks',
        data: graph.data.map((item) => item.value)
      }]
    }
  }
}
