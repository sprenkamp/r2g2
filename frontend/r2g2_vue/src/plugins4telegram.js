import api from './router/api.js'

// define all functions that will be used
export default function Plugin(app) {
  
  app.config.globalProperties.$minDate_tele = null;
  app.config.globalProperties.$maxDate_tele = null;

  // function change language
  app.config.globalProperties.$changeLocale_tele = function(locale) {
    this.$i18n.locale = locale;
  };

//   // get data from database
//   app.config.globalProperties.$getData_tele = async function() {
//     const response = await api.getMongoClusterTest();
//     const data_tele = response.data;
//     return data_tele
//   };

  // function get all cluster categories
  app.config.globalProperties.$getCluster_tele = async function(data_tele) {
    const clusterCategories = Array.from(new Set(data_tele.map((item) => item.cluster)))
    return clusterCategories;
  };

  // function get all state categories
  app.config.globalProperties.$getState_tele = async function(data_tele) {
    const stateCategories = Array.from(new Set(data_tele.map((item) => item.state)))
    return stateCategories;
  };
  
  // function to get all date
  app.config.globalProperties.$getDate_tele = async function(data_tele) {
    const dates = Array.from(new Set(data_tele.map((item) => new Date(item.date))));
    const dateData = Array.from(new Set(data_tele.map((item) => item.date)))
    this.$minDate_tele = new Date(Math.min(...dates)).toISOString().split('T')[0];
    this.$maxDate_tele = new Date(Math.max(...dates)).toISOString().split('T')[0];
    return dateData;
  };

  // function count cluster
  app.config.globalProperties.$countProp_tele = async function(data_tele, targetDate, specifiedCluster) {
    const clustersCount = {};
    data_tele.forEach(item => {
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
  app.config.globalProperties.$countryFilter_tele = async function(data_tele, selectedCountry) {
    return data_tele.filter((item) => {
      const countryMatch = !selectedCountry || item.country === selectedCountry;
      return countryMatch;
    });
  };

  // filter data according to state name
  app.config.globalProperties.$stateFilter_tele = async function(data_tele, selectedState) {
    return data_tele.filter((item) => {
      const stateMatch = !selectedState || item.state === selectedState;
      return stateMatch;
    });
  };
  
  // transfer timestamps to a list of item in format yyyy-MM-dd
  app.config.globalProperties.$convertTimetoString_tele = async function(timestamps) {
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

