import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import translate_app from './data/translate_app.json'
import App from './App.vue';
import router from './router/router';
import axios from "axios";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/css/index.css";
import 'leaflet/dist/leaflet.css';

// language
const i18n = createI18n({
    legacy: true,
    locale: 'English',
    messages: translate_app,
    missingWarn: false
});

const app = createApp(App);
app.config.globalProperties.$axios = axios;
app.use(ElementPlus);
app.use(router);
app.use(i18n)
app.component("Loading", Loading);
app.mount('#app');
