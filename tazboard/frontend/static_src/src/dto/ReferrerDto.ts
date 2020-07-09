import { ChartData } from 'chart.js'

export class ReferrerData {
  referrertag!: string
  hits!: number
  hits_previous!: number
  percentage!: number
  percentage_previous!: number
}

export class ReferrerDto {
  total!: number
  total_previous!: number
  data!: Array<ReferrerData>

  static toChartdata (graph: ReferrerDto): ChartData {
    return {
      labels: graph.data.map((item) => new Date(item.referrertag).toLocaleTimeString(
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
