// plugins.js

// define all functions that will be used
import Papa from 'papaparse';
import * as echarts from 'echarts';

const Plugin = function (app, options) {
  
  app.config.globalProperties.$minDate = null;
  app.config.globalProperties.$maxDate = null;

  // function change language
  app.config.globalProperties.$changeLocale = function(locale) {
    this.$i18n.locale = locale;
  };

  // function handle csv data
  app.config.globalProperties.$handleCSV = async function(path) {
    return new Promise((resolve, reject) => {
      Papa.parse(path, {
        download: true,
        header: true, 
        skipEmptyLines: true,
        complete: (results) => {
          resolve(results.data);
        },
        error: (error) => {
          reject(error);
        },
      });
    });
  };

  // function get all cluster categories
  app.config.globalProperties.$getCluster = async function(path) {
    const csvData = await this.$handleCSV(path);
    const clusterCategories = Array.from(new Set(csvData.map((item) => item.cluster)))
    return clusterCategories;
  };

  // function get all state categories
  app.config.globalProperties.$getState = async function(path) {
    const csvData = await this.$handleCSV(path);
    const stateCategories = Array.from(new Set(csvData.map((item) => item.state)))
    return stateCategories;
  };
  
  // function to get all date
  app.config.globalProperties.$getDate = async function(path) {
    const csvData = await this.$handleCSV(path);
    const dates = Array.from(new Set(csvData.map((item) => new Date(item.date))));
    const dateData = Array.from(new Set(csvData.map((item) => item.date)))
    this.$minDate = new Date(Math.min(...dates)).toISOString().split('T')[0];
    this.$maxDate = new Date(Math.max(...dates)).toISOString().split('T')[0];
    return dateData;
  };

  // function count cluster
  app.config.globalProperties.$countProp = async function(csvData, targetDate, specifiedCluster) {
    const clustersCount = {};
    csvData.forEach(item => {
      const clusters = Array.isArray(item.cluster) ? item.cluster : [item.cluster];
      const date = item.date;
      if (date === targetDate && (!specifiedCluster || clusters.some(cluster => specifiedCluster.includes(cluster)))) {
        clusters.forEach(cluster => {
          if (cluster in clustersCount) {
            clustersCount[cluster]++;
          } else {
            clustersCount[cluster] = 1;
          }
        });
      };
    });
    return clustersCount
  };

  // filter data according to country name
  app.config.globalProperties.$countryFilter = async function(path, selectedCountry) {
    const csvData = await this.$handleCSV(path);
    return csvData.filter((item) => {
      const countryMatch = !selectedCountry || item.country === selectedCountry;
      return countryMatch;
    });
  };

  // filter data according to state name
  app.config.globalProperties.$stateFilter = async function(path, selectedState) {
    const csvData = await this.$handleCSV(path);
    return csvData.filter((item) => {
      const stateMatch = !selectedState || item.state === selectedState;
      return stateMatch;
    });
  };
  
  // transfer timestamps to a list of item in format yyyy-MM-dd
  app.config.globalProperties.$convertTimetoString = async function(timestamps) {
    const startDate = new Date(timestamps[0]);
    const endDate = new Date(timestamps[1]);
    const dateStrings = [];
    let currentDate = startDate;
    while (currentDate <= endDate) {
      dateStrings.push(currentDate.toISOString().split('T')[0]);
      currentDate.setDate(currentDate.getDate() + 1);
    }
    return dateStrings;
  }
};

export default Plugin;
