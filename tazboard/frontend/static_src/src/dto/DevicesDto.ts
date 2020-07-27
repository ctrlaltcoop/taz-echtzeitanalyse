import { ChartData } from 'chart.js'
import { DEVICE_LABEL_UNCLASSIFIED, deviceColors } from '@/common/colors'

export class DevicesData {
  deviceclass!: string
  hits!: number

  static toChartdata (devicesData: Array<DevicesData>): ChartData {
    // sort data descending
    devicesData.sort((a, b) => b.hits - a.hits)
    return {
      labels: devicesData.map((item) => `${item.deviceclass}: ${item.hits}`),
      datasets: [{
        label: 'Devices',
        data: devicesData.map((item) => item.hits),
        barThickness: 20,
        backgroundColor: devicesData.map((item) =>
          deviceColors[item.deviceclass] ?? deviceColors[DEVICE_LABEL_UNCLASSIFIED])
      }]
    }
  }
}

export class DevicesDto {
  data!: Array<DevicesData>
}
