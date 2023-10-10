<template>
    <div class="navigation">
      <Navigation/>
      <el-button @click="toggleSidebar" :icon="sidebarIcon"></el-button>
    </div>
    <el-container class="layout-container">
      <!-- <loading :active="isLoading" :is-full-page="true" :loader="loader" /> -->
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
          <el-col :span="8">
            <MapComponent ref="mapcomponent" class="map-component"
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
            <el-row>
              <div class="empty-line"></div>
            </el-row>
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
            <el-button round @click="drawer = true">
              <Icon icon="material-symbols:robot-2-outline" width="56" height="56" :horizontalFlip="true" />
              <Icon icon="humbleicons:chat" width="36" height="36"/>
            </el-button>
          </template>
        </el-popover>
      </el-container>
    </el-affix>
    <el-drawer v-model="drawer" :with-header="false">
        <template #default>
          <ChatBot/>
        </template>
    </el-drawer>
    <div>
      <DatePicker/>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch, toRefs, getCurrentInstance} from 'vue';
  import MapComponent from './MapComponent.vue';
  import LineChart from './LineChart.vue';
  import ChatBot from './ChatBot.vue';
  import Navigation from './Navigation.vue';
  import { ArrowRight as arrowright, ArrowLeft as arrowleft } from '@element-plus/icons-vue';
  import { Icon } from '@iconify/vue';
  import axios from '../router/request';
  import DatePicker from './DatePicker.vue';
  import {
      getCluster_tele,
      getState_tele,
      getDate_tele,
      countProp_tele,
      countedCluster,
      countryFilter_tele,
      stateFilter_tele,
      convertTimetoString_tele,
      movingAverage,
      minDate_tele,
      maxDate_tele
    } from '../myplugins';
  
  const { emit } = getCurrentInstance();
  const dataTele = ref([]);
  const cachedData = ref({});
  const isLoading = ref(false);
  const fullPage = ref(false);
  const loader = ref('bars');
  const showSidebar = ref(false);
  const sidebarIcon = ref(arrowright);
  const selectedNews = ref(['all found topics']);
  const newsOptions = ref([]);
  const selectedCountry = ref('');
  const countryOptions = ref(['all countries analysed', 'Germany', 'Switzerland']);
  const selectedState = ref('');
  const stateOptions = ref([]);
  const selectedDate = ref(null);
  const selectedDateRange = ref(null);
  const minDate = ref(null);
  const maxDate = ref(null);
  const dateOptions = ref([]);
  const chartData = ref({
    labels: [],
    datasets: [],
  });
  const filteredData = ref([]);
  const drawer = ref(false);
  
  const fetch = async () => {
    if (cachedData.value.dataTele) {
      dataTele.value = cachedData.value.dataTele;
    } else {
      try {
        const response = await axios.get('http://localhost:8000/test/bertopic');
        dataTele.value = response.data;
        cachedData.value.dataTele = dataTele.value;
      } catch (error) {
        console.log(error);
      }
    }
  };
  
  const DtoE = () => {
    if (selectedCountry.value === 'Deutschland') {
      return 'Germany';
    } else if (selectedCountry.value === 'Schweiz') {
      return 'Switzerland';
    } else {
      return selectedCountry.value;
    }
  };
  
  const filterDataByCountryAndState = async () => {
    const countrySelected = DtoE();
    return dataTele.value.filter((item) => {
      const countryMatch = !countrySelected || item.country === countrySelected;
      const stateMatch = !selectedState.value || item.state === selectedState.value;
      return countryMatch && stateMatch;
    });
  };
  
  const handleSliderChange = async (values) => {
    const [minValue, maxValue] = values;
    selectedDateRange.value = await convertTimetoString_tele(values);
    dateOptions.value = selectedDateRange.value;
    updateChartData();
  };
  
  const updateChartData = async () => {
    const selectedCluster = selectedNews.value;
    const ClustersData = {};
    for (const targetDate of dateOptions.value) {
      const clusterCount = await countProp_tele(filteredData.value, targetDate, selectedCluster);
      ClustersData[targetDate] = clusterCount;
    }
  
    const aftermovingAverage = await movingAverage(ClustersData, 21);
    chartData.value = {
      tension: 0.3,
      labels: dateOptions.value,
      datasets: newsOptions.value.map((option) => ({
        tension: 0.3,
        label: option.value,
        data: dateOptions.value.map((date) => aftermovingAverage[date][option.value] || 0),
        borderWidth: 2,
        fill: false,
        pointStyle: false,
      })),
    };
  };
  
  const updateCountryAndState = () => {
    if (selectedCountry.value === 'all countries analysed' || selectedCountry.value === 'alle analysierten Länder') {
      filteredData.value = dataTele.value;
    } else {
      filteredData.value = filterDataByCountryAndState();
    }
    updateChartData();
  };
  
  const handleCountryAndStateChanged = ({ selectedCountry, selectedState }) => {
    selectedCountry.value = selectedCountry;
    selectedState.value = selectedState;
  };
  
  const handleStateSelected = (selectedState) => {
    selectedState.value = selectedState;
  };
  
  const toggleSidebar = () => {
    showSidebar.value = !showSidebar.value;
    sidebarIcon.value = showSidebar.value ? arrowleft : arrowright;
  }
  
  onMounted(async () => {
    isLoading.value = true;
    await fetch();
  
    // get all cluster in array like {1:xx, 2:yy, ...}
    const clusteredData = await getCluster_tele(dataTele.value);
    newsOptions.value = clusteredData.map((cluster) => ({
      value: cluster,
    }));
    selectedNews.value = newsOptions.value.map((option) => option.value);
  
    // get all state
    const stateData = await getState_tele(dataTele.value);
    stateOptions.value = stateData.map((state) => ({
      value: state,
    }));
  
    // get the min, max date as well as date range in type 1645660800000
    const dateData = await getDate_tele(dataTele.value);
    dateOptions.value = dateData;
    await getDate_tele(dataTele.value)
    .then(() => {
      minDate.value = new Date(minDate_tele).getTime();
      maxDate.value = new Date(maxDate_tele).getTime();
      selectedDate.value = [minDate.value, maxDate.value];
    });
  
    // Load data and draw chart
    const allClustersData = {};
    for (const targetDate of dateOptions.value) {
      const allClustersCount = await countedCluster(dataTele.value, targetDate);
      allClustersData[targetDate] = allClustersCount;
    }
  
    // moving average
    const aftermovingAverage = await movingAverage(allClustersData, 21);
  
    chartData.value = {
      labels: dateOptions.value,
      datasets: newsOptions.value.map((option) => ({
        tension: 0.3,
        label: option.value,
        data: dateOptions.value.map((date) => aftermovingAverage[date][option.value] || 0),
        borderWidth: 2,
        fill: false,
        pointStyle: false,
      })),
    };
    filteredData.value = await filterDataByCountryAndState();
    isLoading.value = false;
  });
  
  watch(selectedNews, () => {
    updateChartData();
  }, {immediate: true});
  watch([selectedCountry, selectedState], () => {
    updateCountryAndState();
  });
  watch(() => [selectedCountry.value, selectedState.value], () => {
    emit('countryAndStateChanged', {
      selectedCountry: selectedCountry.value,
      selectedState: selectedState.value
    });
  });
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
  </style>