import Vue from 'vue'

import BaseDashboardTable from '@/views/base/BaseDashboardTable.vue'
import { ApiClient } from '@/client/ApiClient'
import { ArticleData } from '@/dto/ToplistDto'
import { Timeframe } from '@/common/timeframe'

const apiClient = new ApiClient()

interface Data {
  items: ArticleData[];
}

interface Methods {
  fetchData(timeframe: Timeframe, signal: AbortSignal): Promise<void>;
}

export default Vue.extend<Data, Methods, {}, {}>({
  name: 'Fireplace',
  extends: BaseDashboardTable,
  methods: {
    async fetchData (timeframe: Timeframe, signal: AbortSignal) {
      this.items = (
        await apiClient.fireplace(
          timeframe.minDate(),
          timeframe.maxDate(),
          null,
          {
            signal
          })).data
    }
  }
})
