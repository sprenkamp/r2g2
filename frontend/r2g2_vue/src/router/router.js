import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Telegram from '../components/Telegram.vue'
import Test from '../components/Test.vue'

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
  {
    path: "/Test",
    name: 'Test',
    component: Test
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router
