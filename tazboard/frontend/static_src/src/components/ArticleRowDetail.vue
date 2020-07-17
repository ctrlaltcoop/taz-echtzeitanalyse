<template>
  <div class="article-row-detail mr-5 ml-5 pb-3 row">
    <div class="histogram col-4 h-100 d-flex">
      <GraphContainer class="card-shadow" :chart-component="histogramChartComponent" :graph-data="histogram" :options="histogramGraphOptions" />
    </div>
    <div class="devices col-4">
      <GraphContainer :chart-component="devicesChartComponent" :graph-data="article.devices" />
    </div>
    <div class="referrers col-4">
      <GraphContainer :chart-component="referrerChartComponent" :graph-data="article.referrers" />
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
import ReferrerBar from '@/components/graphs/charts/ReferrerBar.vue'
import { HistogramData } from '@/dto/HistogramDto'

interface ArticleRowDetailProps {
  article: ArticleData;
}

interface ArticleRowDetailData {
  histogram: Array<HistogramData>;
}

export default Vue.extend<ArticleRowDetailData, {}, {}, ArticleRowDetailProps>({
  name: 'ArticleRowDetail',
  props: {
    article: Object
  },
  data: () => {
    return {
      histogramChartComponent: HistogramLine,
      referrerChartComponent: ReferrerBar,
      devicesChartComponent: DevicesBar,
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
    GraphContainer
  },
  async mounted () {
    const apiClient = new ApiClient()
    this.histogram = (await apiClient.histogram(new Date(this.article.pubdate), new Date(), this.article.msid)).data
  }
})
</script>
<style lang="scss" scoped>
@import "src/style/variables";

.article-row-detail {
  display: flex;
  height: 250px;
}

</style>
