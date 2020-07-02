<template>
  <div ref="container">
    <DailyLineGraph ref="container" :styles="graphStyles" :graph="graph"/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import DailyLineGraph from '@/components/DailyLineGraph.vue'
import { ApiClient } from '@/client/ApiClient'
import { HistogramDto } from '@/dto/HistogramDto'

export interface DailyLineGraphData {
  graph: HistogramDto | null;
  graphStyles: object;
}

export interface TickerMethods {
  resizeGraph(): void;
}

export default Vue.extend<DailyLineGraphData, TickerMethods, {}, {}>({
  name: 'Ticker',
  components: {
    DailyLineGraph
  },
  data: () => {
    return {
      graph: null,
      graphStyles: {}
    }
  },
  methods: {
    resizeGraph () {
      if (this.$refs.container) {
        const height = (this.$refs.container as Element).clientHeight
        const width = (this.$refs.container as Element).clientWidth
        this.graphStyles = {
          width: `${width}px`,
          height: `${height}px`,
          position: 'relative'
        }
      } else {
        this.graphStyles = {}
      }
    }
  },
  async mounted () {
    this.resizeGraph()
    window.addEventListener('resize', () => this.resizeGraph())
    const client = new ApiClient()
    this.graph = await client.histogram('now-24h', 'now')
  },
  destroyed () {
    window.removeEventListener('resize', () => this.resizeGraph())
  }
})
</script>
