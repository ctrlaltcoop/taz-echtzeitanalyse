import { subDays, subHours, subMinutes } from 'date-fns'

export enum TimeframeId {
  KEY_15_MINUTES = '15_MINUTES',
  KEY_30_MINUTES = '30_MINUTES',
  KEY_1_HOURS = '1_HOURS',
  KEY_6_HOURS = '6_HOURS',
  KEY_24_HOURS = '24_HOURS',
  KEY_7_DAYS = '7_DAYS',
  KEY_30_DAYS = '30_DAYS'
}

export interface Timeframe {
  id: TimeframeId;
  label: string;
  minDate: () => Date;
  maxDate: () => Date;
}

export const TIMEFRAMES: Array<Timeframe> = [{
  id: TimeframeId.KEY_15_MINUTES,
  label: '15 minuten',
  minDate: () => subMinutes(new Date(), 15),
  maxDate: () => new Date()
}, {
  id: TimeframeId.KEY_30_MINUTES,
  label: '30 Minuten',
  minDate: () => subMinutes(new Date(), 30),
  maxDate: () => new Date()
}, {
  id: TimeframeId.KEY_1_HOURS,
  label: '1 Stunde',
  minDate: () => subHours(new Date(), 1),
  maxDate: () => new Date()
}, {
  id: TimeframeId.KEY_6_HOURS,
  label: '6 Stunden',
  minDate: () => subHours(new Date(), 6),
  maxDate: () => new Date()
}, {
  id: TimeframeId.KEY_24_HOURS,
  label: '24 Stunden',
  minDate: () => subHours(new Date(), 24),
  maxDate: () => new Date()
}, {
  id: TimeframeId.KEY_7_DAYS,
  label: '7 Tage',
  minDate: () => subDays(new Date(), 7),
  maxDate: () => new Date()
}, {
  id: TimeframeId.KEY_30_DAYS,
  label: '30 Tage',
  minDate: () => subDays(new Date(), 30),
  maxDate: () => new Date()
}]

export function getTimeframeById (timeframeId: TimeframeId): Timeframe | undefined {
  return TIMEFRAMES.find(({ id }) => id === timeframeId)
}

export const DEFAULT_TIMEFRAME: Timeframe = TIMEFRAMES[0]
