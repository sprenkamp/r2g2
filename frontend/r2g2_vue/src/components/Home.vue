<!-- Home.vue -->

<template>
  <div class="navigation">
    <Navigation/>
    <el-button @click="toggleSidebar">
      <Icon
        :icon="showSidebar ? 'material-symbols:play-arrow-outline' : 'material-symbols:play-arrow-outline'"
        :rotate="showSidebar ? 2 : 0"
      />
    </el-button>
  </div>
  <el-container class="layout-container">
    <el-aside width="300px" v-show="showSidebar">
      <el-scrollbar>
        <!-- 数据类别选择框/topics selection box -->
        <div class="m-4">
          <h3>{{$t('Choose the topics of interest within the telegram data')}}</h3>
          <el-select
            v-model="selectedNews"
            multiple
            collapse-tags
            collapse-tags-tooltip
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
        <el-row>
          <div class="empty-line"></div>
        </el-row>
      </el-scrollbar>
    </el-aside>

    <!-- 主页面/main -->
    <el-main>
      <el-row class="header">
        <h1>{{$t('Identification of the most relevant topics in the context of the Ukrainian Refugee Crisis in the media and social media')}}</h1>
      </el-row>
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
          <DatePicker v-if="minDate !== null && maxDate !== null" :minDate="minDate" :maxDate="maxDate" @selected-date="handleSelectedDate"/>
          <!-- <el-slider v-model="selectedDate" :min="minDate" :max="maxDate" range @change="handleSliderChange"/> -->
        </el-col>
      </el-row>
      <!-- 第二行 空行/second row, empty line -->
      <el-row>
        <div class="empty-line"></div>
      </el-row>
      <!-- 第三行/third row -->
      <el-row>
        <!-- 第三行第一列 地图/first column in third row, map -->
        <el-col :span="8">
          <MapComponent ref="mapcomponent" class="map-container"
            :selectedCountry="selectedCountry"
            :selectedState="selectedState"
            @countryAndStateChanged="handleCountryAndStateChanged"
            @stateSelected="handleStateSelected"
          />
        </el-col>
        <!-- 第三行第二列 折线图和chatbot/second column in third row, line chart and chatbot -->
        <el-col :span="16">
          <el-container class="chart-container">
            <LineChart :height="300" :chartData="chartData" :selectedState="selectedState" />
          </el-container>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
  <el-affix position="bottom" :offset="20">
    <el-container class="chatbot">
      <el-popover
        placement="top-start"
        title="Hello!"
        :width="200"
        trigger="hover"
        content="I'm a chatbot, try to ask me some questions.">
        <template #reference>
          <el-button round @click="toggleChatbot">
            <Icon icon="material-symbols:robot-2-outline" width="56" height="56" :horizontalFlip="true" />
            <Icon icon="humbleicons:chat" width="36" height="36"/>
          </el-button>
        </template>
      </el-popover>
    </el-container>
  </el-affix>
  <el-affix position="bottom" :offset="750">
    <el-container class="chatbot-container">
      <ChatBot v-show="showChatbot"/>
    </el-container>
  </el-affix>
</template>

<script>
import MapComponent from './MapComponent.vue';
import LineChart from './LineChart.vue';
import ChatBot from './ChatBot.vue';
import Navigation from './Navigation.vue';
import DatePicker from './DatePicker.vue';
import {
    ArrowRight as arrowright,
    ArrowLeft as arrowleft
} from '@element-plus/icons-vue';
import {Icon} from '@iconify/vue'

export default {
  components: {
    MapComponent,
    LineChart,
    ChatBot,
    Navigation,
    DatePicker,
    arrowright,
    arrowleft,
    Icon,
  },
  data() {
    return {
      isLoading: false,
      fullPage: false,
      loader: "bars",
      showSidebar: false,       // show side bar
      sidebarIcon: arrowright,
      newsPath: 'https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/df_news_demo.csv', // temporary mock data path
      // selectedLanguage: '',    // language property, define the current chosen language in web
      // languageOptions: [ 'English', 'Deutsch'], // define language options in select box
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
      showChatbot: false,
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
    this.minDate = this.dateOptions[0];
    this.maxDate = this.dateOptions[this.dateOptions.length - 1];
    this.selectedDate = [this.minDate, this.maxDate];

    // Load data and draw chart
    this.isLoading = true;
    const allClustersData = {};
    for (const targetDate of this.dateOptions) {
      const csvData = await this.$handleCSV(newsPath);
      const allClustersCount = await this.$countProp(csvData, targetDate);
      allClustersData[targetDate] = allClustersCount;
    };
    
    // console.log(allClustersData)
    // moving average
    // const aftermovingAverage = await this.$movingAverage(allClustersData, 2)
    // console.log(aftermovingAverage)
    this.chartData = {
      labels: this.dateOptions,
      datasets: this.newsOptions.map((option) => ({
        tension: 0.3,
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

    // async handleSliderChange(values) {
    //   const [minValue, maxValue] = values;
    //   this.selectedDateRange = await this.$convertTimetoString(values);
    //   this.dateOptions = this.selectedDateRange;
    //   this.updateChartData();
    // },

    async handleSelectedDate(value) {
      if (value === null) {
        return;
      }
      this.dateOptions = await this.$convertTimetoString(value);
      this.updateChartData();
    },

    async updateChartData() {
      this.selectedCluster = this.selectedNews;
      const ClustersData = {};
      for (const targetDate of this.dateOptions) {
        const clusterCount = await this.$countProp(this.filteredData, targetDate, this.selectedCluster);
        ClustersData[targetDate] = clusterCount;
      }
      // const movingAverage = await this.$movingAverage(ClustersData, 2)
      this.chartData = {
        labels: this.dateOptions,
        datasets: this.newsOptions.map((option) => ({
          tension: 0.3,
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
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
      this.sidebarIcon = this.showSidebar ? arrowleft : arrowright;
    },
    toggleChatbot() {
      this.showChatbot = !this.showChatbot;
    },
  },
};
</script>


<style scoped> 
.navigation {
  position: fixed;
  width: 100%;
  z-index: 100;
  top: 0;
  left: 0;
}
.layout-container {
  padding-top: 50px;
  display: flex;
  flex-grow: 1;
  overflow-x: hidden;
  background-color: transparent;
  height: 100%;
}
.layout-container h3 {
  /* font-family: 'Cantora One', sans-serif; */
  margin-bottom: 30px;
  font-size: 15px;
}
.layout-container .m-4 {
  margin-left: 30px;
  margin-top: 30px;
}
.header {
  height: 100px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: transparent;
}
.layout-container h1 {
  font-family: 'IM Fell English', serif;
  margin: 10px;
  font-size: 30px;
  text-align: center;
  font-size: 28px;
}
.layout-container .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}
.layout-container .el-main {
  padding: 20px;
  flex-grow: 1;
  overflow-y: hidden;
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
.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
  flex-grow: 1;
}
.chatbot {
  justify-content: center;
  /* align-items: center; */
}
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 25%;
  z-index: 999;
}
</style>
