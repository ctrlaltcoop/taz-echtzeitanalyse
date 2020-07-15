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
import { subDays } from 'date-fns'
import GraphContainer from '@/components/GraphContainer.vue'

export interface ReferrerGraphData {
  referrerGraph: ReferrerDto | null;
  graphStyles: object;
}

export default Vue.extend<ReferrerGraphData, {}, {}, {}>({
  name: 'ReferrerContainer',
  components: {
    ReferrerGraph,
    GraphContainer
  },
  data: () => {
    return {
      referrerGraph: null,
      graphStyles: {}
    }
  },
  async mounted () {
    const client = new ApiClient()
    this.referrerGraph = await client.referrer(subDays(new Date(), 1), new Date())
  }
})
</script>
