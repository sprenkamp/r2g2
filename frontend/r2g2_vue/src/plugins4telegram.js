// plugins4telegram.js

// define all functions that will be used
const Plugins = function (app, options) {

  app.config.globalProperties.$minDate_tele = null;
  app.config.globalProperties.$maxDate_tele = null;

  // function change language
  app.config.globalProperties.$changeLocale_tele = function(locale) {
    this.$i18n.locale = locale;
  };

  // function get all cluster categories
  app.config.globalProperties.$getCluster_tele = async function(data_tele) {
    const clusterCategories = Array.from(new Set(data_tele.map((item) => item.predicted_class)))
    // const clusterCategories = Array.from(new Set(data_tele.map((item) => item.cluster_fixed)))
    return clusterCategories;
  };

  // function get all state categories
  app.config.globalProperties.$getState_tele = async function(data_tele) {
    const stateCategories = Array.from(new Set(data_tele.map((item) => item.state)))
    return stateCategories;
  };

  app.config.globalProperties.$getDate_tele = async function(data_tele) {
    const validData = data_tele.filter(item => item.messageDate !== undefined);
    const dates = Array.from(new Set(validData.map((item) => item.messageDate)));
    const dateData = Array.from(new Set(validData.map((item) => item.messageDate)));
    this.$minDate_tele = Math.min(...dates);
    this.$maxDate_tele = Math.max(...dates);
    dateData.sort((a, b) => new Date(a) - new Date(b));
    return dateData;
  };
  

  // function count cluster
  app.config.globalProperties.$countProp_tele = async function(data_tele, targetDate, specifiedCluster) {
    const clustersCount = {};
    data_tele.forEach(item => {
      // const clusters = Array.isArray(item.cluster_fixed) ? item.cluster_fixed : [item.cluster_fixed];
      const clusters = Array.isArray(item.predicted_class) ? item.predicted_class : [item.predicted_class];
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

  // function count cluster with counted data
  app.config.globalProperties.$countedCluster = async function(data_tele, targetDate, specifiedCluster) {
    const clustersCount = {};
    data_tele.forEach(item => {
      const cluster = item.predicted_class;
      const date = item.messageDate;
      const count = item.count;

      if (date === targetDate && (!specifiedCluster || specifiedCluster.includes(cluster))) {
        if (cluster in clustersCount) {
          clustersCount[cluster] += count;
        } else {
          clustersCount[cluster] = count;
        }
      }
    });
    return clustersCount;
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
  };

  app.config.globalProperties.$movingAverage = async function(data, windowSize) {
    const dates = Object.keys(data);
    let movingAverage = {};

    const allClusters = new Set();
    for (const date of dates) {
      for (const cluster in data[date]) {
        allClusters.add(cluster);
      }
    }
    for (const date of dates) {
      movingAverage[date] = {};
      for (const cluster of allClusters) {
        movingAverage[date][cluster] = 0;
      }
    }
    for (let i = windowSize - 1; i < dates.length; i++) {
      const currentDate = dates[i];
      for (const cluster in data[currentDate]) {
        let sum = 0;
        for (let j = i - windowSize + 1; j <= i; j++) {
          const date = dates[j];
          if (cluster in data[date]) {
            sum += data[date][cluster];
          }
        }
        const averageValue = sum / windowSize;
        movingAverage[currentDate][cluster] = averageValue;
      }
    }
    return movingAverage;
  };

};

export default Plugins;