<template>
  <div ref="container">
    <component :is="chartComponent" :options="options" :graph="graphData" :styles="graphStyles" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { BaseChart } from 'vue-chartjs/types/components'
import { ChartData, ChartOptions } from 'chart.js'

interface GraphContainerData {
  graphStyles: object;
}

interface GraphContainerProps {
  chartComponent: BaseChart;
  options: ChartOptions;
  graphData: ChartData;
}

interface GraphContainerMethods {
  resizeGraph(): void;
}

export default Vue.extend<GraphContainerData, GraphContainerMethods, {}, GraphContainerProps>({
  data: () => {
    return {
      graphStyles: {}
    }
  },
  props: {
    chartComponent: Function,
    options: Object,
    graphData: Object
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
