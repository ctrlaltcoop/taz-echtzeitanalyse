import { ReferrerData } from '@/dto/ReferrerDto'

export class ArticleData {
  headline!: string
  kicker!: string
  hits!: number
  hits_previous!: number
  referrers!: Array<ReferrerData>
}

export class ToplistDto {
  total!: number
  data!: Array<ArticleData>
}
