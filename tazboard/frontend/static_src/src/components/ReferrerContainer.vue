<template>
  <GraphContainer>
    <template slot-scope="{graphStyles}">
      <ReferrerGraph ref="containter" :styles="graphStyles" :graph="referrerGraph"/>
    </template>
  </GraphContainer>
</template>

<script lang="ts">
import Vue from 'vue'
import { ReferrerDto } from '@/dto/ReferrerDto'
import { ApiClient } from '@/client/ApiClient'
import ReferrerGraph from '@/components/ReferrerGraph.vue'
import GraphContainer from '@/components/GraphContainer.vue'
import { getTimeframeById, Timeframe } from '@/common/timeframe'

const client = new ApiClient()

export interface ReferrerGraphData {
  referrerGraph: ReferrerDto | null;
  graphStyles: object;
}

interface Methods {
  update(timeframe: Timeframe): void;
}

export default Vue.extend<ReferrerGraphData, Methods, {}, {}>({
  name: 'ReferrerContainer',
  components: {
    ReferrerGraph,
    GraphContainer
  },
  methods: {
    async update (timeframe: Timeframe) {
      this.referrerGraph = await client.referrer(timeframe.minDate, timeframe.maxDate)
    }
  },
  data: () => {
    return {
      referrerGraph: null,
      graphStyles: {}
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
  }
})
</script>
