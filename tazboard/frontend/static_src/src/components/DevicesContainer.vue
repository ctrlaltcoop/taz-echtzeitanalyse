<template>
  <GraphContainer>
    <template slot-scope="{graphStyles}">
      <DevicesGraph ref="containter" :styles="graphStyles" :graph="devicesGraph"/>
    </template>
  </GraphContainer>
</template>

<script lang="ts">
import Vue from 'vue'
import { ApiClient } from '@/client/ApiClient'
import { DevicesDto } from '@/dto/DevicesDto'
import DevicesGraph from '@/components/DevicesGraph.vue'
import GraphContainer from '@/components/GraphContainer.vue'
import { getTimeframeById, Timeframe } from '@/common/timeframe'

const client = new ApiClient()

export interface DevicesGraphData {
  devicesGraph: DevicesDto | null;
  graphStyles: object;
}

interface Methods {
  update(timeframe: Timeframe): void;
}

export default Vue.extend<DevicesGraphData, Methods, {}, {}>({
  name: 'DevicesContainer',
  components: {
    DevicesGraph,
    GraphContainer
  },
  methods: {
    async update (timeframe: Timeframe) {
      this.devicesGraph = await client.devices(timeframe.minDate, timeframe.maxDate)
    }
  },
  data: () => {
    return {
      devicesGraph: null,
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
