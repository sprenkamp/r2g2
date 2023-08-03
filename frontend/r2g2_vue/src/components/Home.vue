<!-- <template>
    <h3>This is home page</h3>
    <el-button color="FFFFFF" type="primary" class="button1">
      <router-link to="/newspage" class="news">news</router-link>
    </el-button>

    <div>
      <h1>{{ $t('Select a country of interest') }}</h1>
      <p>{{ $t("all countries analysed") }}</p>
      <button @click="changeLocale('English')">English</button>
      <button @click="changeLocale('Deutsch')">Deutsch</button>
    </div>
</template>
 -->

<template>
  <el-container class="layout-container" style="height: 700px">
    <el-aside width="400px">
      <el-scrollbar>
        <div class="m-4">
          <p>Sprache/Language</p>
          <el-select v-model="selectedLanguage" class="m-2" placeholder="Select" size="large" @change="$changeLocale(this.selectedLanguage)">
            <el-option
              v-for="item in languageOptions"
              :key="item"
              :value="item"
            />
          </el-select>
        </div>
        <div class="m-4">
          <p>{{$t('Choose the topics of interest within the news data')}}</p>
          <el-select
            v-model="selectedNews"
            multiple
            placeholder="Select"
            size="large"
          >
            <el-option
              v-for="item in newsOptions"
              :key="item.value"
              :value="item.value"
            />
          </el-select>
        </div>

      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-header style="text-align: center; font-size: 25px">
        {{$t('Identification of the most relevant topics in the context of the Ukrainian Refugee Crisis in the media and social media')}}
      </el-header>

      <el-main>
        <el-row>
          <el-col :span="8"><div class="grid-content ep-bg-purple"/>
            <p>{{$t('Select a country of interest')}}</p>
            <el-select v-model="selectedCountry" class="m-2" placeholder="Select" size="large">
              <el-option
                v-for="(country) in countryOptions"
                :key="country"
                :value="country"
              />
            </el-select>
          </el-col>
          <el-col :span="8"><div class="grid-content ep-bg-purple-light" />
            <p>{{$t('Choose a state of interest')}}</p>
            <el-select v-model="selectedState" class="m-2" placeholder="Select" size="large">
              <el-option
                v-for="item in stateOptions"
                :key="item.value"
                :value="item.value"
              />
            </el-select>
          </el-col>
          <el-col :span="8"><div class="grid-content ep-bg-purple" />
            <p>{{$t('Choose date range of interest')}}</p>
            <el-slider v-model="selectedDate" :min="minDate" :max="maxDate" range />
          </el-col>
        </el-row>
      
        <LineChart :chartData="chartData" />
      </el-main>

    </el-container>
  </el-container>
</template>

<script>
// import MapComponent from './MapComponent.vue';
import LineChart from './LineChart.vue'

export default {
  components: {
    // MapComponent
    LineChart,
  },

  data() {
    return {
      selectedLanguage: '',
      languageOptions: [ 'English', 'Deutsch'],
      selectedNews: [],
      newsOptions: [],
      selectedCountry: '', 
      countryOptions: ['all country analysed', 'Germany', 'Switzerland'],
      selectedState: '',
      stateOptions: [],
      selectedDate: null,
      minDate: null,
      maxDate: null,
      dateOptions: [],
      chartData: {
        labels: [],
        datasets: [],
      },
    };
  },

  async created(){
    const newsPath = 'https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/df_news_demo.csv'
    const clusteredData = await this.$getCluster(newsPath);
    this.newsOptions = clusteredData.map((cluster) => ({
      value: cluster,
    }));

    const stateData = await this.$getState(newsPath);
    this.stateOptions = stateData.map((state) => ({
      value: state,
    }));

    const dateData = await this.$getDate(newsPath);
    this.dateOptions = dateData;
    this.$getDate(newsPath)
    .then(() => {
      this.minDate = new Date(this.$minDate).getTime();
      this.maxDate = new Date(this.$maxDate).getTime();
      this.selectedDate = [this.minDate, this.maxDate];
    });

    // Load data and draw chart
    const allClustersData = {};
    for (const targetDate of this.dateOptions) {
      const allClustersCount = await this.$countProp(newsPath, targetDate);
      allClustersData[targetDate] = allClustersCount;
    };

    this.chartData = {
      labels: this.dateOptions,
      datasets: this.newsOptions.map((option) => ({
        label: option.value,
        data: this.dateOptions.map((date) => allClustersData[date][option.value] || 0),
        borderWidth: 2,
        fill: false,
        pointStyle: false,
      }))
    };

    this.updateChartData();
  },

  methods: {
    async updateChartData() {
      const allClustersData = {};
      for (const targetDate of this.dateOptions) {
        const allClustersCount = await this.$countProp(newsPath, targetDate);
        allClustersData[targetDate] = allClustersCount;
      }

      this.chartData = {
        labels: this.dateOptions,
        datasets: this.newsOptions.map((option) => ({
          label: option.value,
          data: this.dateOptions.map((date) => allClustersData[date][option.value] || 0),
          borderWidth: 2,
          fill: false,
          pointStyle: false,
        })),
      };
    },
  },
};
</script>


<style scoped>
.layout-container .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}
.layout-container .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}
.layout-container .el-main {
  padding: 0;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

/* New styles for the map component */
.layout-container .el-main .map-component {
  width: 100%;
  height: 100%;
}

</style>
