import { ChartData } from 'chart.js'

export class DevicesData {
  deviceclass!: string
  hits!: number

  static toChartdata (devicesData: Array<DevicesData>): ChartData {
    // sort data descending
    devicesData.sort((a, b) => b.hits - a.hits)
    return {
      labels: devicesData.map((item) => item.deviceclass),
      datasets: [{
        label: 'Devices',
        data: devicesData.map((item) => item.hits)
      }]
    }
  }
}

export class DevicesDto {
  data!: Array<DevicesData>
}
