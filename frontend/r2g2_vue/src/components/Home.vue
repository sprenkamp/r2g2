<!-- Home.vue -->

<template>
  <el-container class="layout-container" style="height: 100vh">
    <el-aside width="300px">
      <el-scrollbar>
        <el-collapse>
          <el-collapse-item title="Language" name="1">
            <!-- 语言选择框/language selection box-->
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
          </el-collapse-item>
          <el-collapse-item title="News" name="2">
            <!-- 数据类别选择框/topics selection box -->
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
          </el-collapse-item>
          <el-collapse-item title="X" name="3">

          </el-collapse-item>
          <el-collapse-item title="Telegram" name="4">

          </el-collapse-item>
        </el-collapse>

        <!-- 跳转测试页面路由 -->
        <el-button color="FFFFFF" type="primary" class="button1">
          <router-link to="/testpage" class="test">test</router-link>
        </el-button>
      </el-scrollbar>
    </el-aside>

    <el-container>
      <!-- 标题/title -->
      <el-header class="page-header" >
        <h1>{{$t('Identification of the most relevant topics in the context of the Ukrainian Refugee Crisis in the media and social media')}}</h1>
      </el-header>
      <!-- 主页面/main -->
      <el-main>
        <!-- 第一行/first row -->
        <el-row>
          <!-- 第一行第一列 选择国家/first column in first row, select country -->
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
          <!-- 第一行第二列 选择州/second column in first row, select state -->
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
          <!-- 第一行第三列 时间轴/third column in first row, time slider -->
          <el-col :span="8"><div class="grid-content ep-bg-purple" />
            <h3>{{$t('Choose date range of interest')}}</h3>
            <el-slider v-model="selectedDate" :min="minDate" :max="maxDate" range @change="handleSliderChange"/>
          </el-col>
        </el-row>
        <!-- 第二行 空行/second row, empty line -->
        <el-row>
          <div class="empty-line"></div>
        </el-row>
        <!-- 第三行/third row -->
        <el-row>
          <!-- 第三行第一列 地图/first column in third row, map -->
          <el-col :span="11">
            <MapComponent ref="mapcomponent" class="map-component"
              :selectedCountry="selectedCountry"
              :selectedState="selectedState"
              @countryAndStateChanged="handleCountryAndStateChanged"
              @stateSelected="handleStateSelected"
            />
          </el-col>
          <!-- 第三行第二列 折线图和chatbot/second column in third row, line chart and chatbot -->
          <el-col :span="13">
            <loading :active="isLoading" :is-full-page="true" :loader="loader" />
            <LineChart :chartData="chartData" :selectedState="selectedState" />
            <el-row>
              <div class="empty-line"></div>
            </el-row>
            <el-container class="chatbot">
              <el-button type="primary" style="margin-left: 16px" @click="drawer = true">
                Ask Question with Chatbot
              </el-button>
              <el-drawer v-model="drawer" :with-header="false">
                <ChatBot/>
              </el-drawer>
            </el-container>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import MapComponent from './MapComponent.vue';
import LineChart from './LineChart.vue';
import ChatBot from './ChatBot.vue';

export default {
  components: {
    MapComponent,
    LineChart,
    ChatBot,
  },
  data() {
    return {
      isLoading: false,
      fullPage: false,
      loader: "bars",
      newsPath: 'https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/df_news_demo.csv', // temporary mock data path
      selectedLanguage: '',    // language property, define the current chosen language in web
      languageOptions: [ 'English', 'Deutsch'], // define language options in select box
      selectedNews: ['all found topics'], // 
      newsOptions: [],         // store clusters options in data
      selectedCountry: '',     // country property, define the current chosen country in web
      countryOptions: ['all countries analysed', 'Germany', 'Switzerland'], // define country options in select box
      selectedState: '',       // state property, define the current chosen state
      stateOptions: [],        // define state options in select box
      selectedDate: null,      // date property, define the date range in time slider
      selectedDateRange: null, // store new date range when slider move
      minDate: null,           // define min date
      maxDate: null,           // define max date
      dateOptions: [],         // define date options in time slider
      chartData: {
        labels: [],
        datasets: [],
      },                       // define data for line chart
      filteredData: [],        // store filtered data
      drawer: false,
    };
  },

  async created(){
    const newsPath = 'https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/df_news_demo.csv'
    
    // get all cluster in array like {1:xx, 2:yy, ...}
    const clusteredData = await this.$getCluster(newsPath);
    this.newsOptions = clusteredData.map((cluster) => ({
      value: cluster,
    }));
    this.selectedNews = this.newsOptions.map(option => option.value);

    // get all state
    const stateData = await this.$getState(newsPath);
    this.stateOptions = stateData.map((state) => ({
      value: state,
    }));

    // get the min,max date as well as date range in type 1645660800000
    const dateData = await this.$getDate(newsPath);
    this.dateOptions = dateData;
    this.$getDate(newsPath)
    .then(() => {
      this.minDate = new Date(this.$minDate).getTime();
      this.maxDate = new Date(this.$maxDate).getTime();
      this.selectedDate = [this.minDate, this.maxDate];
    });

    // Load data and draw chart
    this.isLoading = true;
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
    this.isLoading = false;
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
        const countryMatch = !countrySelected || item.country === countrySelected;
        const stateMatch = !this.selectedState || item.state === this.selectedState;
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
    handleStateSelected(selectedState) {
      this.selectedState = selectedState;
      // this.$refs.mapcomponent.zoomToSelectedState(selectedState);
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
.chatbot {
  justify-content: center;
  /* align-items: center; */
}
</style>
