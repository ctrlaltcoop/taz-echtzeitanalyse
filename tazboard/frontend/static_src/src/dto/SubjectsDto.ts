import { ReferrerData } from '@/dto/ReferrerDto'
import { DevicesData } from '@/dto/DevicesDto'

export class SubjectsData {
  subject_name!: string
  article_count!: number
  hits!: number
  referrers!: Array<ReferrerData>
  devices!: Array<DevicesData>
}

export class SubjectsDto {
  total!: number
  data!: Array<SubjectsData>
}
