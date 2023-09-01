// api.js

import path from "./path";
import axios from "./request";

export default {

    getMongoTest() {
        return axios.get(path.mongo_test);
    },

    getMongoClusterTest() {
        return axios.get(path.mongo_cluster_test)
    },

    async fetchCluterData() {
        try {
            const response = await axios.get(path.mongo_cluster_test);
            return response.data;
          } catch (error) {
            console.error(error);
            throw new Error('Failed to fetch clustered data');
          }
    },
};