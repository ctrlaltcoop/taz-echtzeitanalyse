import { getISOWeek, isToday, isYesterday } from 'date-fns'
import { CAPTION_YESTERDAY } from '@/common/constants'

export function formatPublicationTime (value: string | null): string {
  if (value === null) return ''
  const now = new Date()
  const pubDate = new Date(value)
  const thisWeek = getISOWeek(now)
  const pubWeek = getISOWeek(pubDate)
  if (isToday(pubDate)) {
    return new Date(value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (isYesterday(pubDate)) {
    return CAPTION_YESTERDAY
  } else if (thisWeek === pubWeek) {
    return new Date(value).toLocaleDateString([], {
      weekday: 'long'
    })
  } else {
    return new Date(value).toLocaleDateString()
  }
}
