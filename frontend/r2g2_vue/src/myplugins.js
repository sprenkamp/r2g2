// myplugins.js

export const changeLocale_tele = function (locale) {
    this.$i18n.locale = locale;
};
  
export const getCluster_tele = async function (data_tele) {
    const clusterCategories = Array.from(new Set(data_tele.map((item) => item.cluster)));
    return clusterCategories;
};
  
export const getState_tele = async function (data_tele) {
    const stateCategories = Array.from(new Set(data_tele.map((item) => item.state)));
    return stateCategories;
};

export let minDate_tele = null;
export let maxDate_tele = null;

export const getDate_tele = async function (data_tele) {
    const dates = Array.from(new Set(data_tele.map((item) => new Date(item.date))));
    const dateData = Array.from(new Set(data_tele.map((item) => item.date)));
    minDate_tele = new Date(Math.min(...dates)).toISOString().split('T')[0];
    maxDate_tele = new Date(Math.max(...dates)).toISOString().split('T')[0];
    dateData.sort((a, b) => new Date(a) - new Date(b));
    return dateData;
};
  
export const countProp_tele = async function (data_tele, targetDate, specifiedCluster) {
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
    return clustersCount;
};
  
  export const countedCluster = async function (data_tele, targetDate, specifiedCluster) {
    const clustersCount = {};
    data_tele.forEach(item => {
      const cluster = item.cluster;
      const date = item.date;
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
  
  export const countryFilter_tele = async function (data_tele, selectedCountry) {
    return data_tele.filter((item) => {
      const countryMatch = !selectedCountry || item.country === selectedCountry;
      return countryMatch;
    });
  };
  
  export const stateFilter_tele = async function (data_tele, selectedState) {
    return data_tele.filter((item) => {
      const stateMatch = !selectedState || item.state === selectedState;
      return stateMatch;
    });
  };
  
  export const convertTimetoString_tele = async function (timestamps) {
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
  
  export const movingAverage = async function (data, windowSize) {
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
  