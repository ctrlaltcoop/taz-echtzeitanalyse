import { ReferrerDto } from '@/dto/ReferrerDto'
import { DevicesDto } from '@/dto/DevicesDto'

export interface Dataset {
  referrers: ReferrerDto;
  devices: DevicesDto;
}

export interface DatasetState {
  current: Dataset | null;
}

export interface UpdateTimeframeParams {
  minDate: Date;
  maxDate: Date;
}

export enum MutationTypes {
  UPDATE_DATASET = 'UPDATE_DATASET',
}

export enum ActionTypes {
  SET_TIMEFRAME = 'SET_TIMEFRAME',
}
