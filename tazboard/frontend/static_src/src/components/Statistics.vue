<template>
  <div class="row statistics-area">
    <div class="col-4 pt-5 pb-5  statistics-box histogram-box">
      <LoadingControl class="card-shadow" :loading-state="loadingStateHistogram">
        <GraphContainer :chart-component="histogramLineComponent" :graph-data="histogramGraph"/>
      </LoadingControl>
    </div>
    <div class="col-4 pt-5 pb-5 statistics-box">
      <ClickCounter class="card-shadow flex-fill"/>
    </div>
    <div class="col-4 pt-5 pb-5 statistics-box">
      <LoadingControl class="card-shadow" :loading-state="loadingStateTimeframe">
        <div class="row no-gutters flex-fill">
          <div class="col-6">
            <p class="statistics-heading">Geräte</p>
            <GraphContainer class="graph-container" :chart-component="deviceBarComponent" :graph-data="devicesGraph"/>
          </div>
          <div class="col-6">
            <p class="statistics-heading">Referrer</p>
            <GraphContainer class="graph-container" :chart-component="referrerBarComponent" :graph-data="referrerGraph"/>
          </div>
        </div>
      </LoadingControl>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

import ClickCounter from '@/components/ClickCounter.vue'
import GraphContainer from '@/components/graphs/GraphContainer.vue'
import LoadingControl from '@/components/LoadingControl.vue'
import ReferrerBar from '@/components/graphs/charts/ReferrerBar.vue'
import HistogramLine from '@/components/graphs/charts/HistogramLine.vue'
import DevicesBar from '@/components/graphs/charts/DevicesBar.vue'
import { getTimeframeById, Timeframe } from '@/common/timeframe'
import { ApiClient } from '@/client/ApiClient'
import { subDays } from 'date-fns'
import { ReferrerData } from '@/dto/ReferrerDto'
import { HistogramData } from '@/dto/HistogramDto'
import { DevicesData } from '@/dto/DevicesDto'
import { LoadingState } from '@/common/LoadingState'

const apiClient = new ApiClient()

interface StatisticsData {
  referrerBarComponent: typeof ReferrerBar;
  deviceBarComponent: typeof DevicesBar;
  histogramLineComponent: typeof HistogramLine;
  referrerGraph: Array<ReferrerData>;
  histogramGraph: Array<HistogramData>;
  devicesGraph: Array<DevicesData>;
  loadingStateTimeframe: LoadingState;
  loadingStateHistogram: LoadingState;
}

interface StatisticsMethods {
  update (timeframe: Timeframe): void;
}

let currentRequestController: AbortController | null = null

export default Vue.extend<StatisticsData, StatisticsMethods, {}, {}>({
  name: 'Statistics',
  components: {
    ClickCounter,
    GraphContainer,
    LoadingControl
  },
  data: () => {
    return {
      referrerBarComponent: ReferrerBar,
      deviceBarComponent: DevicesBar,
      histogramLineComponent: HistogramLine,
      referrerGraph: [],
      histogramGraph: [],
      devicesGraph: [],
      loadingStateTimeframe: LoadingState.FRESH,
      loadingStateHistogram: LoadingState.FRESH
    }
  },
  methods: {
    async update (timeframe: Timeframe) {
      this.loadingStateTimeframe = LoadingState.LOADING
      try {
        if (currentRequestController !== null) {
          currentRequestController.abort()
        }
        currentRequestController = new AbortController()
        const { signal } = currentRequestController!!
        this.referrerGraph = (await apiClient.referrer(timeframe.minDate, timeframe.maxDate, null, {
          signal
        })).data
        this.devicesGraph = (await apiClient.devices(timeframe.minDate, timeframe.maxDate, null, {
          signal
        })).data
        currentRequestController = null
        this.loadingStateTimeframe = LoadingState.SUCCESS
      } catch (e) {
        if (!(e instanceof DOMException)) {
          this.loadingStateTimeframe = LoadingState.ERROR
        }
      }
    }
  },
  watch: {
    '$route.query': {
      handler (query: any, oldQuery: any) {
        if (query.timeframeId !== oldQuery?.timeframeId) {
          const timeframe = getTimeframeById(query.timeframeId)
          this.update(timeframe!!)
        }
      },
      immediate: true,
      deep: true
    }
  },
  async mounted () {
    this.loadingStateHistogram = LoadingState.LOADING
    try {
      this.histogramGraph = (await apiClient.histogram(subDays(new Date(), 1), new Date())).data
      this.loadingStateHistogram = LoadingState.SUCCESS
    } catch (e) {
      if (!(e instanceof DOMException)) {
        this.loadingStateHistogram = LoadingState.ERROR
      }
    }
  }
})
</script>
<style lang="scss">
@import "src/style/variables";

.histogram-box {
  background: $white;
}

.statistics-area {
  background: $gray-200;
}

.statistics-box {
  height: 350px;
  display: flex;
}

.click-counter-area {
  display: flex;
}

.statistics-heading {
  margin-bottom: 3px;
  text-align: center;
}

.graph-container {
  height: 220px;
}

</style>
