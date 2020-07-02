import Vue from 'vue'
import Vuex from 'vuex'
import { dataset } from '@/store/dataset'
import { DatasetState } from '@/store/dataset/types'

Vue.use(Vuex)

export interface RootState {
  dataset: DatasetState;
}

export default new Vuex.Store<RootState>({
  modules: {
    dataset
  }
})
