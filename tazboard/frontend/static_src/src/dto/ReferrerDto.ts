import { ChartData } from 'chart.js'

export class ReferrerData {
  referrerclass!: string
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
      labels: graph.data.map((item) => item.referrerclass),
      datasets: [{
        label: 'Referrers',
        data: graph.data.map((item) => item.hits)
      }]
    }
  }
}
