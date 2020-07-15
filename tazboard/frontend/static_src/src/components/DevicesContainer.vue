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
import { subDays } from 'date-fns'
import GraphContainer from '@/components/GraphContainer.vue'

export interface DevicesGraphData {
  devicesGraph: DevicesDto | null;
  graphStyles: object;
}

export default Vue.extend<DevicesGraphData, {}, {}, {}>({
  name: 'DevicesContainer',
  components: {
    DevicesGraph,
    GraphContainer
  },
  data: () => {
    return {
      devicesGraph: null,
      graphStyles: {}
    }
  },
  async mounted () {
    const client = new ApiClient()
    this.devicesGraph = await client.devices(subDays(new Date(), 1), new Date())
  }
})
</script>
