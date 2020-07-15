<template>
  <div ref="container">
    <slot :graphStyles="graphStyles"></slot>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

interface GraphContainerData {
  graphStyles: object;
}

export interface GraphContainerMethods {
  resizeGraph(): void;
}

export default Vue.extend<GraphContainerData, GraphContainerMethods, {}, {}>({
  data: () => {
    return {
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
  },
  destroyed () {
    window.removeEventListener('resize', () => this.resizeGraph())
  }
})
</script>
