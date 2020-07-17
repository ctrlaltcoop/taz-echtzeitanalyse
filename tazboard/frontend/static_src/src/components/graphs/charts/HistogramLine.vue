<script lang="ts">
import Vue from 'vue'
import { Line } from 'vue-chartjs'
import { HistogramData } from '@/dto/HistogramDto'
import { ChartMethods } from '@/types/chartjs'
import { ChartOptions } from 'chart.js'
import { mergeDeep } from '@/utils/objects'

interface HistogramLineProps {
  graph: Array<HistogramData> | null;
  options: ChartOptions;
}

interface HistogramLineComputed {
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

export default Vue.extend<{}, ChartMethods<HistogramData>, HistogramLineComputed, HistogramLineProps>({
  name: 'HistogramLine',
  extends: Line,
  props: {
    options: {
      type: Object,
      default: null
    },
    graph: {
      type: Array,
      default: null
    }
  },
  computed: {
    graphOptions (): ChartOptions {
      return mergeDeep(DEFAULT_OPTIONS, this.options)
    }
  },
  methods: {
    updateChart (histogramData: Array<HistogramData>) {
      const chartData = HistogramData.toChartdata(histogramData!!.slice())

      chartData.datasets = chartData.datasets?.map((dataset) => {
        return {
          ...dataset,
          backgroundColor: GRAPH_BACKGROUND_COLOR,
          borderColor: GRAPH_LINE_COLOR
        }
      })
      // @ts-ignore i failed to make the parent functions visible to typescript
      this.renderChart(chartData, this.graphOptions)
    }
  },
  watch: {
    graph: {
      handler (newVal: Array<HistogramData> | null) {
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
