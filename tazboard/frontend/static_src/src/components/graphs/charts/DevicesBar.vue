<script lang="ts">
import Vue from 'vue'
import { HorizontalBar } from 'vue-chartjs'
import { ChartOptions } from 'chart.js'
import { ChartMethods } from '@/types/chartjs'
import { DevicesData } from '@/dto/DevicesDto'
import { FIXED_BAR_DISPLAY_COUNT } from '@/common/constants'

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
      if (data.length < FIXED_BAR_DISPLAY_COUNT) {
        for (let i = data.length; i < FIXED_BAR_DISPLAY_COUNT; i++) {
          data.push({})
        }
      }
      const chartData = DevicesData.toChartdata(data!!.slice())

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
