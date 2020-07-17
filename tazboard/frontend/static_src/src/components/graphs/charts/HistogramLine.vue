<script lang="ts">
import Vue from 'vue'
import { Line } from 'vue-chartjs'
import { HistogramDto } from '@/dto/HistogramDto'
import { VueChartMethods } from '@/types/chartjs'
import { ChartOptions } from 'chart.js'
import { mergeDeep } from '@/utils/objects'

export interface DailyLineGraphProps {
  graph: HistogramDto | null;
  options: ChartOptions;
}

export interface DailyLineGraphComputed {
  graphOptions: ChartOptions;
}

const GRAPH_BACKGROUND_COLOR = '#7DD2D2'
const GRAPH_LINE_COLOR = '#FFFFFF'

const DEFAULT_OPTIONS = {
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
} as ChartOptions

export default Vue.extend<{}, VueChartMethods, DailyLineGraphComputed, DailyLineGraphProps>({
  name: 'DailyLineGraph',
  extends: Line,
  props: {
    options: {
      type: Object,
      default: null
    },
    graph: {
      type: Object,
      default: null
    }
  },
  computed: {
    graphOptions (): ChartOptions {
      return mergeDeep(DEFAULT_OPTIONS, this.options)
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
        this.renderChart(chartData, this.graphOptions)
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
