<!-- LineChart.vue -->

<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script>
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, TimeScale, Colors} from 'chart.js';
import 'chartjs-adapter-date-fns';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, TimeScale, Colors)

export default {
  name: 'LineChart',
  components: { Line },
  props: {
    chartData: {
      type: Object,
      required: true
    },
    selectedState: String, // add chosen state as prop
    chartOptions: {
      type: Object,
      default: () => ({
        // maintainAspectRatio: false,
        // width: 10,
        // height: 10,
        responsive: true,
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day',
              displayFormats: {
                day: 'yyyy-MM-dd',
              },
            },
            title: {
              display: true,
              text: 'Date',
              fontSize: 16,
            },
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Count',
              fontSize: 16,
            },
          },
        },
        plugins: {
          title: {
            display: true,
            text: 'Title',
            fontSize: 20,
          },
          legend: {
            position: 'top'
          },
        },
      })
    }
  },
  computed: {
    filteredChartData() {
      if (!this.selectedState) {
        return this.chartData;
      }
      // 根据选中的州过滤数据，然后返回过滤后的数据
      return {
        ...this.chartData,
        datasets: this.chartData.datasets.map((dataset) => ({
          ...dataset,
          tension: 0.3,
          data: dataset.data.map((value, index) => ({
            x: dataset.data[index].x,
            y: value.x === this.selectedState ? value.y : 0,
          })),
        })),
      };
    },
  },
}
</script>