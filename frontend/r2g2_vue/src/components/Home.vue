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
  <el-container class="layout-container" style="height: 100vh">
    <el-aside width="300px">
      <el-scrollbar>
        <div class="m-4">
          <h3>Sprache/Language</h3>
          <el-select v-model="selectedLanguage" class="m-2" placeholder="Select" size="large" @change="$changeLocale(this.selectedLanguage)">
            <el-option
              v-for="item in languageOptions"
              :key="item"
              :value="item"
            />
          </el-select>
        </div>
        <div class="m-4">
          <h3>{{$t('Choose the topics of interest within the news data')}}</h3>
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
      <el-header class="page-header" >
        <h1>{{$t('Identification of the most relevant topics in the context of the Ukrainian Refugee Crisis in the media and social media')}}</h1>
      </el-header>

      <el-main>
        <el-row>
          <el-col :span="8"><div class="grid-content ep-bg-purple"/>
            <h3>{{$t('Select a country of interest')}}</h3>
            <el-select v-model="selectedCountry" class="m-2" placeholder="Select" size="large" clearable>
              <el-option
                v-for="(country) in countryOptions"
                :key="$t(country)"
                :value="$t(country)"
              />
            </el-select>
          </el-col>
          <el-col :span="8"><div class="grid-content ep-bg-purple-light" />
            <h3>{{$t('Choose a state of interest')}}</h3>
            <el-select v-model="selectedState" class="m-2" placeholder="Select" size="large" clearable>
              <el-option
                v-for="item in stateOptions"
                :key="item.value"
                :value="item.value"
              />
            </el-select>
          </el-col>
          <el-col :span="8"><div class="grid-content ep-bg-purple" />
            <h3>{{$t('Choose date range of interest')}}</h3>
            <el-slider v-model="selectedDate" :min="minDate" :max="maxDate" range @change="handleSliderChange"/>
          </el-col>
        </el-row>
        <el-row>
          <div class="empty-line"></div>
        </el-row>
        <el-row>
          <el-col :span="11">
            <MapComponent class="map-component"
              :selectedCountry="selectedCountry"
              :selectedState="selectedState"
              @countryAndStateChanged="handleCountryAndStateChanged"
            />
          </el-col>
          <el-col :span="13">
            <LineChart :chartData="chartData" />
          </el-col>
        </el-row>
      </el-main>

    </el-container>
  </el-container>
</template>

<script>
import MapComponent from './MapComponent.vue';
import LineChart from './LineChart.vue'

export default {
  components: {
    MapComponent,
    LineChart,
  },

  data() {
    return {
      newsPath: 'https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/df_news_demo.csv',
      selectedLanguage: '',
      languageOptions: [ 'English', 'Deutsch'],
      selectedNews: ['all found topics'],
      newsOptions: [],
      selectedCluster: null,
      selectedCountry: '',
      countryOptions: ['all countries analysed', 'Germany', 'Switzerland'],
      selectedState: '',
      stateOptions: [],
      selectedDate: null,
      selectedDateRange: null,
      minDate: null,
      maxDate: null,
      dateOptions: [],
      chartData: {
        labels: [],
        datasets: [],
      },
      filteredData: [],
      filteredStateOptions: [],
    };
  },

  async created(){
    const newsPath = 'https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/df_news_demo.csv'
    const clusteredData = await this.$getCluster(newsPath);
    
    this.newsOptions = clusteredData.map((cluster) => ({
      value: cluster,
    }));
    this.selectedNews = this.newsOptions.map(option => option.value);

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
      console.log(this.minDate)
    });

    // Load data and draw chart
    const allClustersData = {};
    for (const targetDate of this.dateOptions) {
      const csvData = await this.$handleCSV(newsPath);
      const allClustersCount = await this.$countProp(csvData, targetDate);
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

    this.filteredData = await this.filterDataByCountryAndState();

  },

  watch: {
    selectedNews: {
      immediate: true,
      handler: 'updateChartData',
    },
    selectedCountryAndState() {
      this.$emit('countryAndStateChanged', {
        selectedCountry: this.selectedCountry,
        selectedState: this.selectedState
      });
    },
    selectedCountry: 'updateCountryAndState',
    selectedState: 'updateCountryAndState',
  },

  methods:{
    DtoE() {
      if (this.selectedCountry === 'Deutschland') {
        return 'Germany'
      } else if (this.selectedCountry === 'Schweiz') {
        return 'Switzerland'
      } else {
        return this.selectedCountry
      }
    },
    async filterDataByCountryAndState() {
      const csvData = await this.$handleCSV(this.newsPath);
      const countrySelected = this.DtoE(this.selectedCountry);
      return csvData.filter((item) => {
        console.log(this.countrySelected)
        const countryMatch = !countrySelected || item.country === countrySelected;
        const stateMatch = !this.selectedState || item.state === this.selectedState;
        // const countryMatch = !this.selectedCountry || item.country === this.selectedCountry;
        // const stateMatch = !this.selectedState || item.state === this.selectedState;
        return countryMatch && stateMatch;
      });
    },

    async handleSliderChange(values) {
      const [minValue, maxValue] = values;
      this.selectedDateRange = await this.$convertTimetoString(values);
      this.dateOptions = this.selectedDateRange;
      this.updateChartData();
    },

    async updateChartData() {
      this.selectedCluster = this.selectedNews;
      const ClustersData = {};
      for (const targetDate of this.dateOptions) {
        const clusterCount = await this.$countProp(this.filteredData, targetDate, this.selectedCluster);
        ClustersData[targetDate] = clusterCount;
      }

      this.chartData = {
        labels: this.dateOptions,
        datasets: this.newsOptions.map((option) => ({
          label: option.value,
          data: this.dateOptions.map((date) => ClustersData[date][option.value] || 0),
          borderWidth: 2,
          fill: false,
          pointStyle: false,
        }))
      };
    },

    async updateCountryAndState() {
      if (this.selectedCountry === ('all countries analysed')) {
        this.filteredData = await this.$handleCSV(this.newsPath);
      } else if (this.selectedCountry === ('alle analysierten Länder')) {
        this.filteredData = await this.$handleCSV(this.newsPath);
      } else {
        this.filteredData = await this.filterDataByCountryAndState();
      }
      this.updateChartData();
    },
    handleCountryAndStateChanged({ selectedCountry, selectedState }) {
      this.selectedCountry = selectedCountry;
      this.selectedState = selectedState;
    },
  },
};
</script>


<style scoped> 
.layout-container {
  display: flex;
  background-color: #f0f2f5;
}
.layout-container h3 {
  margin-bottom: 30px;
  font-size: 16px;
}
.layout-container .m-4 {
  margin-left: 30px;
  margin-top: 30px;
}
.layout-container .el-header {
  height: 100px;
  display: grid;
  place-items: center;
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}
.page-header h1 {
  margin: 10px;
  font-size: 24px;
}
.layout-container .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}
.layout-container .el-main {
  padding: 20px;
  overflow-y: auto;
}
.grid-content {
  border-radius: 10px;
  min-height: 10px;
}
.empty-line{
  height: 50px;
}
/* New styles for the map component */
.map-component {
  width: 100%;
  height: 100%;
}

</style>
