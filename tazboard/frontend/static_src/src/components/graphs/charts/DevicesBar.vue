<script lang="ts">
import Vue from 'vue'
import { HorizontalBar } from 'vue-chartjs'
import { ChartOptions } from 'chart.js'
import { ChartMethods } from '@/types/chartjs'
import { DevicesData } from '@/dto/DevicesDto'

export interface DevicesBarProps {
  graph: Array<DevicesData> | null;
}

export interface DeviceBarData {
  options: ChartOptions;
}

export default Vue.extend<DeviceBarData, ChartMethods<DevicesData>, {}, DevicesBarProps>({
  name: 'DevicesBar',
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
            display: false,
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            categoryPercentage: 0.9,
            gridLines: {
              display: false
            }
          }]
        }
      }
    }
  },
  methods: {
    updateChart (data: Array<DevicesData>) {
      const chartData = DevicesData.toChartdata(data!!.slice())

      chartData.datasets = chartData.datasets?.map((dataset) => {
        return {
          barPercentage: 1,
          ...dataset
        }
      })
      // @ts-ignore i failed to make the parent functions visible to typescript
      this.renderChart(chartData, this.options)
    }
  },
  watch: {
    graph: {
      handler (newVal: Array<DevicesData> | null) {
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
