<template>
  <div class="article-row-detail mr-5 ml-5 pb-3 row">
    <div class="histogram col-4 h-100 d-flex">
      <GraphContainer :chart-component="histogramChartComponent" :graph-data="histogram" />
    </div>
    <div class="devices-referrers col-8">

    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { subDays } from 'date-fns'

import GraphContainer from './graphs/GraphContainer.vue'
import HistogramLine from './graphs/charts/HistogramLine.vue'
import { ApiClient } from '@/client/ApiClient'
import { ArticleData } from '@/dto/ToplistDto'

interface ArticleRowDetailProps {
  article: ArticleData;
}

interface ArticleRowDetailData {
  histogram: object;
}

export default Vue.extend<ArticleRowDetailData, {}, {}, ArticleRowDetailProps>({
  name: 'ArticleRowDetail',
  props: {
    article: Object
  },
  data: () => {
    return {
      histogramChartComponent: HistogramLine,
      histogram: {},
      graphOptions: {
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
    this.histogram = await apiClient.histogram(subDays(new Date(), 1), new Date(), this.article.msid)
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
