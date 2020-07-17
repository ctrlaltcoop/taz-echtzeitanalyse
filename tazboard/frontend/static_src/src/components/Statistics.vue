<template>
  <div class="row statistics-area">
    <div class="col-4 pt-5 pb-5  statistics-box">
      <GraphContainer :chart-component="histogramLineComponent" :graph-data="histogramGraph" />
    </div>
    <div class="col-4 pt-5 pb-5 statistics-box">
      <ClickCounter class="card-shadow flex-fill"/>
    </div>
    <div class="col-4 pt-5 pb-5 statistics-box">
      <div class="row no-gutters card-shadow flex-fill">
        <div class="col-6">
          <GraphContainer :chart-component="deviceBarComponent" :graph-data="devicesGraph" />
        </div>
        <div class="col-6">
          <GraphContainer :chart-component="referrerBarComponent" :graph-data="referrerGraph" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

import ClickCounter from '@/components/ClickCounter.vue'
import GraphContainer from '@/components/graphs/GraphContainer.vue'
import ReferrerBar from '@/components/graphs/charts/ReferrerBar.vue'
import HistogramLine from '@/components/graphs/charts/HistogramLine.vue'
import DevicesBar from '@/components/graphs/charts/DevicesBar.vue'
import { getTimeframeById, Timeframe } from '@/common/timeframe'
import { ApiClient } from '@/client/ApiClient'
import { subDays } from 'date-fns'

const apiClient = new ApiClient()

export default Vue.extend({
  name: 'Statistics',
  components: {
    ClickCounter,
    GraphContainer
  },
  data: () => {
    return {
      referrerBarComponent: ReferrerBar,
      deviceBarComponent: DevicesBar,
      histogramLineComponent: HistogramLine,
      referrerGraph: {},
      histogramGraph: {},
      devicesGraph: {}
    }
  },
  methods: {
    async update (timeframe: Timeframe) {
      this.referrerGraph = await apiClient.referrer(timeframe.minDate, timeframe.maxDate)
      this.devicesGraph = await apiClient.devices(timeframe.minDate, timeframe.maxDate)
    }
  },
  watch: {
    '$route.query': {
      handler (query: any) {
        if (query.timeframeId) {
          const timeframe = getTimeframeById(query.timeframeId)
          this.update(timeframe!!)
        }
      },
      immediate: true,
      deep: true
    }
  },
  async mounted () {
    this.histogramGraph = await apiClient.histogram(subDays(new Date(), 1), new Date())
  }
})
</script>
<style lang="scss">
@import "src/style/variables";

.statistics-area {
  background: $gray-200;
}

.statistics-box {
  height: 300px;
  display: flex;
}

.click-counter-area {
  display: flex;
}

</style>
