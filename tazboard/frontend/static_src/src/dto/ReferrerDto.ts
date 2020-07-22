import { ChartData } from 'chart.js'
import { referrerColors, REFERRER_LABEL_UNBEKANNT } from '@/common/colors'

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
        data: referrerData.map((item) => item.hits),
        barThickness: 20,
        backgroundColor: referrerData.map((item) =>
          referrerColors[item.referrer] ?? referrerColors[REFERRER_LABEL_UNBEKANNT])
      }]
    }
  }
}

export class ReferrerDto {
  total!: number
  data!: Array<ReferrerData>
}
