import { ChartData } from 'chart.js'
import { referrerColors, REFERRER_LABEL_UNBEKANNT } from '@/common/colors'

export class ReferrerData {
  referrer!: string
  hits!: number
  percentage!: number

  static toChartdata (referrerData: Array<ReferrerData>): ChartData {
    // sort data descending
    referrerData.sort((a, b) => b.hits - a.hits)

    if (referrerData.length > 8) {
      const remainingReferrersAggregated = {
        referrer: 'andere',
        hits: referrerData.slice(7, referrerData.length)
          .map((item) => item.hits)
          .reduce((a, b) => a + b),
        percentage: referrerData.slice(7, referrerData.length)
          .map((item) => item.percentage)
          .reduce((a, b) => a + b)
      }
      referrerData = referrerData.slice(0, 7)
      referrerData.push(remainingReferrersAggregated)
    }

    return {
      labels: referrerData.map((item) => `${item.referrer}: ${item.hits}`),
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
