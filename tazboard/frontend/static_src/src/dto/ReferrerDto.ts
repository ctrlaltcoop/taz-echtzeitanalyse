import { ChartData } from 'chart.js'

export class ReferrerData {
  referrer!: string
  hits!: number
  percentage!: number

  static toChartdata (referrerData: Array<ReferrerData>): ChartData {
    // sort data descending
    referrerData.sort((a, b) => b.hits - a.hits)
    return {
      labels: referrerData.map((item) => item.referrer),
      datasets: [{
        label: 'Referrers',
        data: referrerData.map((item) => item.hits)
      }]
    }
  }
}

export class ReferrerDto {
  total!: number
  data!: Array<ReferrerData>
}
