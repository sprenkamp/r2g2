import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Telegram from '../components/Telegram.vue'

const routes = [
  {
    path: "/",
    name: 'Home',
    component: Home,
  },
  {
    path: "/Telegram",
    name: 'Telegram',
    component: Telegram
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router
