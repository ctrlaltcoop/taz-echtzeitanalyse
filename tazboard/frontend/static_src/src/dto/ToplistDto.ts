import { ReferrerData } from '@/dto/ReferrerDto'
import { DevicesData } from '@/dto/DevicesDto'

export class ArticleData {
  msid!: number
  headline!: string
  kicker!: string
  pubdate!: string
  hits!: number
  bid!: number
  hits_previous!: number
  referrers!: Array<ReferrerData>
  devices!: Array<DevicesData>
  archive!: boolean
  frontpage!: boolean
  frontpage_position!: number | null
  url!: string
}

export class ToplistDto {
  total!: number
  data!: Array<ArticleData>
}
