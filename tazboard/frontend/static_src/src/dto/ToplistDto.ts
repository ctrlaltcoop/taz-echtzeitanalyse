export class ArticleData {
  name!: string
  value!: number
}

export class ToplistDto {
  total!: number
  data!: Array<ArticleData>
}
