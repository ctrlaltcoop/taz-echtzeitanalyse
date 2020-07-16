<script lang="ts">
import Vue from 'vue'
import { HorizontalBar } from 'vue-chartjs'
import { ChartOptions } from 'chart.js'
import { ReferrerDto } from '../dto/ReferrerDto'
import { VueChartMethods } from '../types/chartjs'

export interface ReferrerGraphProps {
  graph: ReferrerDto | null;
}

export interface ReferrerGraphData {
  options: ChartOptions;
}

export default Vue.extend<ReferrerGraphData, VueChartMethods, {}, ReferrerGraphProps>({
  name: 'ReferrerGraph',
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
      const chartData = ReferrerDto.toChartdata(newVal)

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
