<template>
  <div>
    <div class="row-detail mr-5 ml-5 pb-3 row">
      <div class="histogram col-4 h-100">
        <p class="tazboard-detail-caption">Verlauf seit Veröffentlichung (max. 1 Woche)</p>
        <LoadingControl :loading-state="loadingState">
          <GraphContainer class="tazboard-card-shadow tazboard-graph-container w-100"
                          :chart-component="histogramChartComponent"
                          :graph-data="histogram"
                          :options="histogramGraphOptions"
                          label="Pageviews"
          />
        </LoadingControl>
      </div>
      <div class="devices col-4">
        <p class="tazboard-detail-caption">Geräte</p>
        <GraphContainer class="graph-container" :chart-component="devicesChartComponent"
                        :graph-data="item.devices"/>
      </div>
      <div class="referrers col-4">
        <p class="tazboard-detail-caption">Referrer</p>
        <GraphContainer class="tazboard-graph-container" :chart-component="referrerChartComponent"
                        :graph-data="item.referrers"/>
      </div>
    </div>
    <div class="row">
      <div class="col-12 align-items-end flex-column d-flex">
        <a class="btn btn-danger" target="_blank" :href="cmsLink" v-if="cmsLink">Im Redaktionssystem öffnen</a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

import GraphContainer from '../graphs/GraphContainer.vue'
import HistogramLine from '../graphs/charts/HistogramLine.vue'
import DevicesBar from '@/components/graphs/charts/DevicesBar.vue'
import LoadingControl from '@/components/LoadingControl.vue'
import ReferrerBar from '@/components/graphs/charts/ReferrerBar.vue'
import { HistogramData } from '@/dto/HistogramDto'
import { LoadingState } from '@/common/LoadingState'
import { GlobalPulse, PULSE_EVENT } from '@/common/GlobalPulse'
import { ReferrerData } from '@/dto/ReferrerDto'
import { DevicesData } from '@/dto/DevicesDto'
import { CMS_BASE_LINK } from '@/common/constants'
import { CONNECTION_ALERT_EVENT, ConnectionAlertBus } from '@/common/ConnectionAlertBus'

interface Props {
  item: {
    bid: number;
    referrers: Array<ReferrerData>;
    devices: Array<DevicesData>;
  };
}

interface Data {
  histogram: Array<HistogramData>;
  loadingState: LoadingState;
}

interface Methods {
  updateHistogram (): Promise<void>;
}

interface Computed {
  cmsLink: string | null;
}

export default Vue.extend<Data, Methods, Computed, Props>({
  name: 'BaseRowDetail',
  props: {
    item: Object
  },
  data () {
    return {
      histogramChartComponent: HistogramLine,
      referrerChartComponent: ReferrerBar,
      devicesChartComponent: DevicesBar,
      loadingState: LoadingState.FRESH,
      histogram: [],
      referrers: [],
      devices: [],
      histogramGraphOptions: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
              suggestedMax: 0
            }
          }]
        }
      }
    }
  },
  components: {
    GraphContainer,
    LoadingControl
  },
  async mounted () {
    await this.updateHistogram()
    GlobalPulse.$on(PULSE_EVENT, this.updateHistogram)
  },
  methods: {
    async updateHistogram () {
      this.loadingState = this.loadingState !== LoadingState.SUCCESS ? LoadingState.LOADING : LoadingState.UPDATING
      try {
        // @ts-ignore fetchHistogram should be implemented in subclass -
        // @ts-ignore no proper way to define abstract methods on vue components
        await this.fetchHistogram()
        this.loadingState = LoadingState.SUCCESS
      } catch (e) {
        if (!(e instanceof DOMException)) {
          if (this.loadingState === LoadingState.UPDATING) {
            ConnectionAlertBus.$emit(CONNECTION_ALERT_EVENT)
          } else {
            this.loadingState = LoadingState.ERROR
          }
        }
      }
    }
  },
  computed: {
    cmsLink (): string | null {
      if (this.item.bid !== null) {
        return CMS_BASE_LINK + this.item.bid
      } else {
        return null
      }
    }
  }
})
</script>
<style lang="scss" scoped>
@import "src/style/variables";

.row-detail {
  display: flex;
  height: 250px;
  margin-bottom: 1em;
}

.graph-container {
  height: 220px;
}

</style>
