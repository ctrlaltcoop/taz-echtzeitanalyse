import { ChartData } from 'chart.js'

export class DevicesData {
  deviceclass!: string
  value!: number
}

export class DevicesDto {
  data!: Array<DevicesData>

  static toChartData (graph: DevicesDto): ChartData {
    // sort data descending
    graph.data.sort((a, b) => b.value - a.value)
    return {
      labels: graph.data.map((item) => item.deviceclass),
      datasets: [{
        label: 'Devices',
        data: graph.data.map((item) => item.value)
      }]
    }
  }
}
