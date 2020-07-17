<script lang="ts">
import Vue from 'vue'
import { HorizontalBar } from 'vue-chartjs'
import { ChartOptions } from 'chart.js'
import { ReferrerData } from '@/dto/ReferrerDto'
import { VueChartMethods } from '@/types/chartjs'

export interface ReferrerGraphProps {
  graph: Array<ReferrerData> | null;
}

export interface ReferrerGraphData {
  options: ChartOptions;
}

export default Vue.extend<ReferrerGraphData, VueChartMethods, {}, ReferrerGraphProps>({
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
  watch: {
    graph (newVal) {
      const chartData = ReferrerData.toChartdata(newVal.slice())

      chartData.datasets = chartData.datasets?.map((dataset) => {
        return {
          ...dataset
        }
      })
      if (newVal !== null) {
        this.renderChart(chartData, this.options)
      } else {
        this.renderChart({})
      }
    }
  }
})
</script>
