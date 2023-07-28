// define all functions that will be used
import Papa from 'papaparse';

export default function Plugin(app, options) {
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
        const clusterCategories = Array.from(new Set(csvData.map((row) => row.cluster)))
        return clusterCategories;
    };

    // function get all state categories
    app.config.globalProperties.$getState = async function(path) {
        const csvData = await this.$handleCSV(path);
        const stateCategories = Array.from(new Set(csvData.map((row) => row.state)))
        return stateCategories;
    };
    
    // find min and max date
    app.config.globalProperties.$getDate = async function(path) {
        const csvData = await this.$handleCSV(path);
        const dates = csvData.map((item) => new Date(item.date));
        const minDate = new Date(Math.min(...dates)).toISOString().split('T')[0];
        const maxDate = new Date(Math.max(...dates)).toISOString().split('T')[0];
        return {minDate, maxDate};
    };
};

