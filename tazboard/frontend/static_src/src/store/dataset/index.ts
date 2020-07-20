import { ActionContext, Module } from 'vuex'
import { ActionTypes, Dataset, DatasetState, MutationTypes, UpdateTimeframeParams } from '@/store/dataset/types'
import { ApiClient } from '@/client/ApiClient'

const apiClient = new ApiClient()
let currentAbortController: AbortController | null = null

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
      currentAbortController?.abort()
      currentAbortController = new AbortController()
      const { signal } = currentAbortController
      const referrers = await apiClient.referrer(parameters.minDate, parameters.maxDate, null, { signal })
      commit(MutationTypes.UPDATE_DATASET, {
        ...state.current,
        referrers
      })
    }
  }
}
