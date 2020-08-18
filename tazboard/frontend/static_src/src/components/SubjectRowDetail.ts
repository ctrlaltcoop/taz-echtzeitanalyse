import Vue from 'vue'

import { subDays } from 'date-fns'
import { ApiClient } from '@/client/ApiClient'
import { Timeframe } from '@/common/timeframe'
import BaseRowDetail from '@/components/base/BaseRowDetail.vue'
import { HistogramData } from '@/dto/HistogramDto'
import { SubjectsData } from '@/dto/SubjectsDto'
import { ReferrerData } from '@/dto/ReferrerDto'
import { DevicesData } from '@/dto/DevicesDto'

const apiClient = new ApiClient()

interface Props {
  item: SubjectsData;
}

interface Data {
  histogram: Array<HistogramData>;
  referrers: Array<ReferrerData>;
  devices: Array<DevicesData>;
}

interface Methods {
  fetchHistogram(timeframe: Timeframe, signal: AbortSignal): Promise<void>;
}

export default Vue.extend<Data, Methods, {}, Props>({
  name: 'SubjectRowDetail',
  props: {
    item: Object
  },
  extends: BaseRowDetail,
  methods: {
    async fetchHistogram () {
      this.histogram = (await apiClient.histogram(
        subDays(new Date(), 1),
        new Date(),
        null,
        this.item.subject_name
      )).data
    }
  }
})
