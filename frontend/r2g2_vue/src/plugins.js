// define all functions that will be used
import Papa from 'papaparse';
import * as echarts from 'echarts';

export default function Plugin(app, options) {

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
    app.config.globalProperties.$countProp = async function(path, targetDate, specifiedCluster = null) {
      const csvData = await this.$handleCSV(path);
      const clustersCount = {};
      csvData.forEach(item => {
        const cluster = item.cluster;
        const date = item.date;
        if (date === targetDate && (!specifiedCluster || cluster === specifiedCluster)) {
          if (cluster in clustersCount) {
            clustersCount[cluster]++;
          }
          else {
            clustersCount[cluster] = 1;
          }
        };

      });
      return clustersCount
    };

};

