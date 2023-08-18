import path from "./path";
import axios from "./request";

export default {

    getMongoTest() {
        return axios.get(path.mongo_test);
    },
};