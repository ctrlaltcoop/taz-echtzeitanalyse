import Vue from 'vue'

import BaseDashboardTable from '@/views/base/BaseDashboardTable.vue'
import { ApiClient } from '@/client/ApiClient'
import { Timeframe } from '@/common/timeframe'
import { ArticleData } from '@/dto/ToplistDto'
import { NUM_ARTICLES_TOP_LIST } from '@/common/constants'

const apiClient = new ApiClient()

interface Data {
  items: ArticleData[];
}

interface Methods {
  fetchData(timeframe: Timeframe, signal: AbortSignal): Promise<void>;
}

export default Vue.extend<Data, Methods, {}, {}>({
  name: 'Toplist',
  extends: BaseDashboardTable,
  methods: {
    async fetchData (timeframe: Timeframe, signal: AbortSignal) {
      this.items = (
        await apiClient.toplist(
          timeframe.minDate(),
          timeframe.maxDate(),
          NUM_ARTICLES_TOP_LIST,
          null,
          {
            signal
          })).data
    }
  }
})
