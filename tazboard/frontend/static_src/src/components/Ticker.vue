<template>
  <GraphContainer>
    <template slot-scope="{graphStyles}">
      <DailyLineGraph ref="container" :graph="graph" :style="graphStyles"/>
    </template>
  </GraphContainer>
</template>

<script lang="ts">
import Vue from 'vue'
import DailyLineGraph from '@/components/DailyLineGraph.vue'
import GraphContainer from '@/components/GraphContainer.vue'
import { ApiClient } from '@/client/ApiClient'
import { HistogramDto } from '@/dto/HistogramDto'
import { subDays } from 'date-fns'

export interface DailyLineGraphData {
  graph: HistogramDto | null;
}

export default Vue.extend<DailyLineGraphData, {}, {}, {}>({
  name: 'Ticker',
  components: {
    DailyLineGraph,
    GraphContainer
  },
  data: () => {
    return {
      graph: null,
      graphStyles: {}
    }
  },
  async mounted () {
    const client = new ApiClient()
    this.graph = await client.histogram(subDays(new Date(), 1), new Date())
  }
})
</script>
