export type QueryParams = { [key: string]: string | number | null }

export function queryString (params: QueryParams): string {
  const queryString = Object
    .keys(params)
    .map(k => {
      return params[k] === null ? null : `${encodeURIComponent(k)}=${encodeURIComponent(params[k]!!)}`
    })
    .filter((item) => item !== null)
    .join('&')
  return queryString ? `?${queryString}` : ''
}
