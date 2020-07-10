import { ReferrerData, ReferrerDto } from '@/dto/ReferrerDto'

export class ArticleData {
  headline!: string
  kicker!: string
  pubdate!: string
  hits!: number
  hits_previous!: number
  referrers!: ReferrerDto
}

export class ToplistDto {
  total!: number
  data!: Array<ArticleData>
}
