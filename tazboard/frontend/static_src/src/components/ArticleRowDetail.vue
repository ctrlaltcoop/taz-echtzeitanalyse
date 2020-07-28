<template>
  <div class="article-row-detail mr-5 ml-5 pb-3 row">
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
      <GraphContainer class="graph-container-devices" :chart-component="devicesChartComponent" :graph-data="article.devices"/>
    </div>
    <div class="referrers col-4">
      <p class="bars-heading">Referrer</p>
      <GraphContainer class="graph-container" :chart-component="referrerChartComponent" :graph-data="article.referrers"/>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

import GraphContainer from './graphs/GraphContainer.vue'
import HistogramLine from './graphs/charts/HistogramLine.vue'
import { ApiClient } from '@/client/ApiClient'
import { ArticleData } from '@/dto/ToplistDto'
import DevicesBar from '@/components/graphs/charts/DevicesBar.vue'
import LoadingControl from '@/components/LoadingControl.vue'
import ReferrerBar from '@/components/graphs/charts/ReferrerBar.vue'
import { HistogramData } from '@/dto/HistogramDto'
import { LoadingState } from '@/common/LoadingState'

interface Props {
  article: ArticleData;
}

interface Data {
  histogram: Array<HistogramData>;
  loadingState: LoadingState;
}

export default Vue.extend<Data, {}, {}, Props>({
  name: 'ArticleRowDetail',
  props: {
    article: Object
  },
  data () {
    return {
      histogramChartComponent: HistogramLine,
      referrerChartComponent: ReferrerBar,
      devicesChartComponent: DevicesBar,
      loadingState: LoadingState.FRESH,
      histogram: [],
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
    const apiClient = new ApiClient()
    this.loadingState = LoadingState.LOADING
    try {
      this.histogram = (await apiClient.histogram(new Date(this.article.pubdate), new Date(), this.article.msid)).data
      this.loadingState = LoadingState.SUCCESS
    } catch (e) {
      if (!(e instanceof DOMException)) {
        this.loadingState = LoadingState.ERROR
      }
    }
  }
})
</script>
<style lang="scss" scoped>
@import "src/style/variables";

.article-row-detail {
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
