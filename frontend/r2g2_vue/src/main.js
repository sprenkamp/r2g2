import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router';
import axios from "axios";
import ElementPlus from "element-plus";
import Loading from "vue-loading-overlay";


const app = createApp(App);
app.config.globalProperties.$axios = axios;
app.use(ElementPlus);
app.use(router);
app.component("Loading", Loading);
app.mount('#app');
