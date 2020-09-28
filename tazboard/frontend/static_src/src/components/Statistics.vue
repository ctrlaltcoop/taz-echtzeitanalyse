<template>
  <div class="statistics-area row">
    <div class="col-4 pb-4 d-flex flex-column statistics-box histogram-box">
      <div class="caption-space justify-content-center text-center align-items-center d-flex">
        <h6 class="font-weight-bold m-0">Tagesverlauf der letzten 24h (Besucher*innen gesamt)</h6>
      </div>
      <LoadingControl
        class="p-2 taz-board tazboard-card-shadow statistics-card flex-row d-flex align-items-center justify-content-center"
        :loading-state="loadingStateHistogram">
        <GraphContainer class="histogram-container flex-fill w-100 h-100"
                        :chart-component="histogramLineComponent"
                        :graph-data="histogramGraph"
                        :options="histogramGraphOptions"/>
      </LoadingControl>
    </div>
    <div class="col-4 pb-4 statistics-box d-flex flex-column">
      <div class="caption-space"></div>
      <ClickCounter class="tazboard-card-shadow statistics-card flex-fill"/>
    </div>
    <div class="col-4 pb-4 statistics-box d-flex flex-column">
      <div class="caption-space"></div>
      <LoadingControl class="tazboard-card-shadow statistics-card" :loading-state="loadingStateTimeframe">
        <div class="row no-gutters flex-fill">
          <div class="col-6">
            <p class="statistics-heading">Geräte</p>
            <GraphContainer class="graph-container" :chart-component="deviceBarComponent"
                            :graph-data="devicesGraph"/>
          </div>
          <div class="col-6">
            <p class="statistics-heading">Referrer</p>
            <GraphContainer class="tazboard-graph-container" :chart-component="referrerBarComponent"
                            :graph-data="referrerGraph"/>
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
import { getTimeframeById, Timeframe, TimeframeId } from '@/common/timeframe'
import { ApiClient } from '@/client/ApiClient'
import { subDays } from 'date-fns'
import { ReferrerData } from '@/dto/ReferrerDto'
import { HistogramData } from '@/dto/HistogramDto'
import { DevicesData } from '@/dto/DevicesDto'
import { LoadingState } from '@/common/LoadingState'
import { GlobalPulse, PULSE_EVENT } from '@/common/GlobalPulse'
import { CONNECTION_ALERT_EVENT, ConnectionAlertBus } from '@/common/ConnectionAlertBus'

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
  updateData (timeframe: Timeframe): Promise<void>;

  updateHistogram (): Promise<void>;
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
      loadingStateHistogram: LoadingState.FRESH,
      histogramGraphOptions: {
        scales: {
          xAxes: [{
            ticks: {
              autoSkip: false,
              callback: function (value: any, index: number, values: string[] | number[]) {
                if (index === 0 ||
                  index === Math.floor(values.length / 3) ||
                  index === Math.floor(values.length * 2 / 3) ||
                  index === values.length - 1) {
                  return value.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit'
                  })
                }
              }
            }
          }]
        }
      }
    }
  },
  methods: {
    async updateData (timeframe: Timeframe) {
      this.loadingStateTimeframe = this.loadingStateTimeframe !== LoadingState.SUCCESS ? LoadingState.LOADING : LoadingState.UPDATING
      try {
        if (currentRequestController !== null) {
          currentRequestController.abort()
        }
        currentRequestController = new AbortController()
        const { signal } = currentRequestController!!
        const referrerFetch = apiClient.referrer(timeframe.minDate(), timeframe.maxDate(), null, {
          signal
        })
        const devicesFetch = apiClient.devices(timeframe.minDate(), timeframe.maxDate(), null, {
          signal
        })
        const results = await Promise.all([referrerFetch, devicesFetch])

        this.referrerGraph = results[0].data
        this.devicesGraph = results[1].data
        currentRequestController = null
        this.loadingStateTimeframe = LoadingState.SUCCESS
      } catch (e) {
        if (!(e instanceof DOMException)) {
          if (this.loadingStateTimeframe === LoadingState.UPDATING) {
            ConnectionAlertBus.$emit(CONNECTION_ALERT_EVENT)
          } else {
            this.loadingStateTimeframe = LoadingState.ERROR
          }
        }
      }
    },
    async updateHistogram () {
      this.loadingStateHistogram = this.loadingStateHistogram !== LoadingState.SUCCESS ? LoadingState.LOADING : LoadingState.UPDATING
      try {
        this.histogramGraph = (await apiClient.histogram(subDays(new Date(), 1), new Date())).data
        this.loadingStateHistogram = LoadingState.SUCCESS
      } catch (e) {
        if (!(e instanceof DOMException)) {
          if (this.loadingStateHistogram === LoadingState.UPDATING) {
            ConnectionAlertBus.$emit(CONNECTION_ALERT_EVENT)
          } else {
            this.loadingStateHistogram = LoadingState.ERROR
          }
        }
      }
    }
  },
  watch: {
    '$route.query': {
      handler (query: any, oldQuery: any) {
        if (query.timeframeId !== oldQuery?.timeframeId) {
          const timeframe = getTimeframeById(query.timeframeId)
          this.updateData(timeframe!!)
        }
      },
      immediate: true,
      deep: true
    }
  },
  async mounted () {
    await this.updateHistogram()
    GlobalPulse.$on(PULSE_EVENT, () => {
      this.updateHistogram()
      const timeframe = getTimeframeById(this.$route.query.timeframeId as TimeframeId)
      if (timeframe) {
        this.updateData(timeframe)
      }
    })
  }
})
</script>
<style lang="scss" scoped>
@import "src/style/variables";

.caption-space {
  height: 1.8rem;
}

.histogram-box {
  background: $white;
}

.statistics-area {
  background: $gray-200;
}

.statistics-card {
  height: 230px;
  display: flex;
}

.statistics-heading {
  margin: 15px 0 0 0;
  line-height: 0;
  font-size: 0.9rem;
  font-weight: bold;
  text-align: center;
}

.graph-container {
  height: 220px;
}

</style>
