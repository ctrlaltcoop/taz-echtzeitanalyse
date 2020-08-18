import Vue from 'vue'

import { ApiClient } from '@/client/ApiClient'
import { ArticleData } from '@/dto/ToplistDto'
import { Timeframe } from '@/common/timeframe'
import BaseRowDetail from '@/components/base/BaseRowDetail.vue'
import { HistogramData } from '@/dto/HistogramDto'

const apiClient = new ApiClient()

interface Props {
  item: ArticleData;
}

interface Data {
  histogram: Array<HistogramData>;
}

interface Methods {
  fetchHistogram(timeframe: Timeframe, signal: AbortSignal): Promise<void>;
}

export default Vue.extend<Data, Methods, {}, Props>({
  name: 'ArticleRowDetail',
  props: {
    item: Object
  },
  extends: BaseRowDetail,
  methods: {
    async fetchHistogram () {
      this.histogram = (await apiClient.histogram(new Date(this.item.pubdate), new Date(), this.item.msid)).data
    }
  }
})
