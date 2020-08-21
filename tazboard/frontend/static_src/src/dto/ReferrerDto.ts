import { ChartData } from 'chart.js'
import { referrerColors, REFERRER_LABEL_UNBEKANNT } from '@/common/colors'
import { FIXED_BAR_DISPLAY_COUNT, MISC_REFERRER_KEY } from '@/common/constants'

export class ReferrerData {
  referrer!: string
  hits!: number
  percentage!: number

  static toChartdata (referrerData: Array<ReferrerData>): ChartData {
    const miscReferrers = referrerData.find(({ referrer }) => referrer === MISC_REFERRER_KEY)
    referrerData = referrerData.filter(({ referrer }) => referrer !== MISC_REFERRER_KEY)
    // sort data descending
    referrerData.sort((a, b) => b.hits - a.hits)
    const displayableData = referrerData.slice(0, FIXED_BAR_DISPLAY_COUNT - 1)
    const remainingData = referrerData.slice(FIXED_BAR_DISPLAY_COUNT - 1, referrerData.length)
    if (miscReferrers) {
      remainingData.push(miscReferrers)
    }
    if (referrerData.length > FIXED_BAR_DISPLAY_COUNT) {
      const remainingReferrersAggregated = {
        referrer: 'andere',
        hits: remainingData
          .map((item) => item.hits)
          .reduce((a, b) => a + b),
        percentage: remainingData
          .map((item) => item.percentage)
          .reduce((a, b) => a + b)
      }
      referrerData = displayableData
      referrerData.push(remainingReferrersAggregated)
    }

    return {
      labels: referrerData.map((item) => `${item.referrer}`),
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
