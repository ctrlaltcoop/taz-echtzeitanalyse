<script lang="ts">
import Vue from 'vue'
import { HorizontalBar } from 'vue-chartjs'
import { ChartOptions } from 'chart.js'
import { VueChartMethods } from '@/types/chartjs'
import { DevicesData } from '@/dto/DevicesDto'

export interface DevicesGraphProps {
  graph: Array<DevicesData> | null;
}

export interface DevicesGraphData {
  options: ChartOptions;
}

export default Vue.extend<DevicesGraphData, VueChartMethods, {}, DevicesGraphProps>({
  name: 'DebvicesBar',
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
      const chartData = DevicesData.toChartdata(newVal.slice())

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
