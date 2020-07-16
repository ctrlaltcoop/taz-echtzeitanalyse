<script lang="ts">
import Vue from 'vue'
import { HorizontalBar } from 'vue-chartjs'
import { ChartOptions } from 'chart.js'
import { VueChartMethods } from '@/types/chartjs'
import { DevicesDto } from '@/dto/DevicesDto'

export interface DevicesGraphProps {
  graph: DevicesDto | null;
}

export interface DevicesGraphData {
  options: ChartOptions;
}

export default Vue.extend<DevicesGraphData, VueChartMethods, {}, DevicesGraphProps>({
  name: 'DevicesGraph',
  extends: HorizontalBar,
  props: {
    graph: {
      type: Object,
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
      const chartData = DevicesDto.toChartData(newVal)

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
