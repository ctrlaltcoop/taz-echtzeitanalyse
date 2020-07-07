<template>
  <div ref="container">
    <ReferrerGraph ref="container" :styles="graphStyles" :graph="referrerGraph"/>
    <!-- <DevicesGraph ref="container" :styles="graphStyles" :graph="devicesGraph"/> -->
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { ReferrerDto } from '@/dto/ReferrerDto'
import { ApiClient } from '@/client/ApiClient'
// import { DevicesDto } from "@/dto/DevicesDto";
import ReferrerGraph from '@/components/ReferrerGraph.vue'
// import DevicesGraph from '@/components/DevicesGraph.vue'

export interface ReferrerGraphData {
  referrerGraph: ReferrerDto | null;
  graphStyles: object;
}

// export interface DevicesGraphData {
//   graph: DevicesDto | null;
//   graphStyles: object;
// }

export interface ReferrerDevicesMethods {
  resizeGraph(): void;
}

export default Vue.extend<ReferrerGraphData, ReferrerDevicesMethods, {}, {}>({
  name: 'ReferrerDevices',
  components: {
    ReferrerGraph
    // DevicesGraph
  },
  data: () => {
    return {
      referrerGraph: null,
      // devicesGraph: null,
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
    this.referrerGraph = await client.referrer('now-24h', 'now')
    // this.devicesGraph = await client.devices('now-24h', 'now')
  },
  destroyed () {
    window.removeEventListener('resize', () => this.resizeGraph())
  }
})
</script>
