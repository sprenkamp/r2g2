<template>
    <h3>This is newsPage</h3>
    <el-button color="FFFFFF" type="primary" class="button1">
        <router-link to="/" class="back">back</router-link>
    </el-button>
    <div class="chart-container" style="width: 400px; height: 300px;">
        <Line :data="data" :options="options" />
    </div>
    
</template>

<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'
import * as mock from '../data/mock.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

export default {
  components: {
    Line
  },
  data() {
    return mock
  }
}
</script>

<style>
.chart-container {
  width: 400px;
  height: 300px;
}
</style>