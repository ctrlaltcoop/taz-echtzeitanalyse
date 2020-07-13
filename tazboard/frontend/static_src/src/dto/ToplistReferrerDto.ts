import { ChartData } from 'chart.js'

export class ToplistReferrerData {
  referrertag!: string
  hits!: number
  hits_previous!: number
  percentage!: number
  percentage_previous!: number
}

export class ToplistReferrerDto {
  total!: number
  total_previous!: number
  data!: Array<ToplistReferrerData>
}
