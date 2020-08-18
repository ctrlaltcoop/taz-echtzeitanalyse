<template>
  <div class="row-detail mr-5 ml-5 pb-3 row">
    <div class="histogram col-4 h-100 d-flex">
      <LoadingControl :loading-state="loadingState">
        <GraphContainer class="card-shadow"
                        :chart-component="histogramChartComponent"
                        :graph-data="histogram"
                        :options="histogramGraphOptions"/>
      </LoadingControl>
    </div>
    <div class="devices col-4">
      <p class="bars-heading">Geräte</p>
      <GraphContainer class="graph-container-devices" :chart-component="devicesChartComponent"
                      :graph-data="item.devices"/>
    </div>
    <div class="referrers col-4">
      <p class="bars-heading">Referrer</p>
      <GraphContainer class="graph-container" :chart-component="referrerChartComponent"
                      :graph-data="item.referrers"/>
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

interface Props {
  item: {
    referrers: Array<ReferrerData>;
    devices: Array<DevicesData>;
  };
}

interface Data {
  histogram: Array<HistogramData>;
  loadingState: LoadingState;
}

interface Methods {
  updateHistogram(): Promise<void>;
}

export default Vue.extend<Data, Methods, {}, Props>({
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
    GlobalPulse.$on(PULSE_EVENT, this.updateData)
  },
  methods: {
    async updateHistogram () {
      this.loadingState = LoadingState.LOADING
      try {
        // @ts-ignore fetchHistogram should be implemented in subclass -
        // @ts-ignore no proper way to define abstract methods on vue components
        await this.fetchHistogram()
        this.loadingState = LoadingState.SUCCESS
      } catch (e) {
        if (!(e instanceof DOMException)) {
          this.loadingState = LoadingState.ERROR
        }
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
}

.bars-heading {
  margin-bottom: 3px;
  text-align: center;
}

.graph-container {
  height: 220px;
}

.graph-container-devices {
  height: 120px;
}

</style>
