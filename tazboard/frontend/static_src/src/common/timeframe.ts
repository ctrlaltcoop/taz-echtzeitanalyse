import { subDays, subMinutes, subMonths } from 'date-fns'

export enum TimeframeId {
  KEY_10_MINUTES = '10_MINUTES',
  KEY_1_DAY = '1_DAY',
  KEY_1_MONTH = '1_MONTH'
}

export interface Timeframe {
  id: TimeframeId;
  label: string;
  minDate: Date;
  maxDate: Date;
}

export const TIMEFRAMES: Array<Timeframe> = [{
  id: TimeframeId.KEY_10_MINUTES,
  label: '10 minuten',
  minDate: subMinutes(new Date(), 10),
  maxDate: new Date()
}, {
  id: TimeframeId.KEY_1_DAY,
  label: 'Heute',
  minDate: subDays(new Date(), 1),
  maxDate: new Date()
}, {
  id: TimeframeId.KEY_1_MONTH,
  label: '1 Monat',
  minDate: subMonths(new Date(), 1),
  maxDate: new Date()
}]

export function getTimeframeById (timeframeId: TimeframeId): Timeframe | undefined {
  return TIMEFRAMES.find(({ id }) => id === timeframeId)
}

export const DEFAULT_TIMEFRAME: Timeframe = TIMEFRAMES[0]
