<script lang="ts">
import Vue from 'vue'
import { HorizontalBar } from 'vue-chartjs'
import { ChartOptions } from 'chart.js'
import { ReferrerData } from '@/dto/ReferrerDto'
import { ChartMethods } from '@/types/chartjs'

export interface ReferrerGraphProps {
  graph: Array<ReferrerData> | null;
}

export interface ReferrerGraphData {
  options: ChartOptions;
}

export default Vue.extend<ReferrerGraphData, ChartMethods<ReferrerData>, {}, ReferrerGraphProps>({
  name: 'ReferrerBar',
  extends: HorizontalBar,
  props: {
    graph: {
      type: Array,
      default: null
    }
  },
  data: () => {
    return {
      options: {
        maintainAspectRatio: false,
        responsive: true,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            gridLines: {
              display: false
            }
          }]
        }
      }
    }
  },
  methods: {
    updateChart (histogramData: Array<ReferrerData>) {
      const chartData = ReferrerData.toChartdata(histogramData!!.slice())

      chartData.datasets = chartData.datasets?.map((dataset) => {
        return {
          ...dataset
        }
      })
      // @ts-ignore i failed to make the parent functions visible to typescript
      this.renderChart(chartData, this.options)
    }
  },
  watch: {
    graph: {
      handler (newVal: Array<ReferrerData> | null) {
        if (newVal !== null) {
          this.updateChart(newVal)
        }
      }
    }
  },
  mounted () {
    if (this.graph !== null) {
      this.updateChart(this.graph)
    }
  }
})

</script>
