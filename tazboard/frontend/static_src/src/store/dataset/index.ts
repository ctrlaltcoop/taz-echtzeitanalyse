import { ActionContext, Module } from 'vuex'
import { ActionTypes, Dataset, DatasetState, MutationTypes, UpdateTimeframeParams } from '@/store/dataset/types'
import { ApiClient } from '@/client/ApiClient'

const apiClient = new ApiClient()

export const dataset: Module<DatasetState, {}> = {
  state: {
    current: null
  },
  mutations: {
    [MutationTypes.UPDATE_DATASET] (state: DatasetState, updatedDataset: Dataset) {
      state.current = updatedDataset
    }
  },
  actions: {
    async [ActionTypes.SET_TIMEFRAME] ({ state, commit }: ActionContext<DatasetState, {}>, parameters: UpdateTimeframeParams) {
      const referrers = await apiClient.referrer(parameters.min, parameters.max)
      commit(MutationTypes.UPDATE_DATASET, {
        ...state.current,
        referrers
      })
    }
  }
}
