import { ToplistReferrerDto } from '@/dto/ToplistReferrerDto'

export class ArticleData {
  headline!: string
  kicker!: string
  pubdate!: string
  hits!: number
  hits_previous!: number
  referrers!: ToplistReferrerDto
}

export class ToplistDto {
  total!: number
  data!: Array<ArticleData>
}
