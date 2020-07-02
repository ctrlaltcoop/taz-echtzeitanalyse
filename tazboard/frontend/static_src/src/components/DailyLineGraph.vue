<script lang="ts">
import Vue from 'vue'
import { Line } from 'vue-chartjs'
import { HistogramDto } from '@/dto/HistogramDto'
import { VueChartMethods } from '@/types/chartjs'
import { ChartOptions } from 'chart.js'

export interface DailyLineGraphProps {
  graph: HistogramDto | null;
}

export interface DailyLineGraphData {
  options: ChartOptions;
}

const GRAPH_BACKGROUND_COLOR = '#7DD2D2'
const GRAPH_LINE_COLOR = '#FFFFFF'

export default Vue.extend<DailyLineGraphData, VueChartMethods, {}, DailyLineGraphProps>({
  name: 'DailyLineGraph',
  extends: Line,
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
        elements: {
          point: {
            radius: 2
          }
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false
            },
            ticks: {
              autoSkip: true
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
              suggestedMax: 10000
            },
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
      const chartData = HistogramDto.toChartdata(newVal)

      chartData.datasets = chartData.datasets?.map((dataset) => {
        return {
          ...dataset,
          backgroundColor: GRAPH_BACKGROUND_COLOR,
          borderColor: GRAPH_LINE_COLOR
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

<style scoped>
.chartjs-render-monitor {
  background: #D9D9D9;
}
</style>
