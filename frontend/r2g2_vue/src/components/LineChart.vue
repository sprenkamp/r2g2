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
      chartOptions: {
        type: Object,
        default: () => ({
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
            },
            y: {
              beginAtZero: true,
            },
          },
        })
      }
    },
  }
  
  </script>
  