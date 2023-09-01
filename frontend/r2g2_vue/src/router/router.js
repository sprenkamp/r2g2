import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
import testPage from '../components/testPage.vue'
import TelegramPage from '../components/TelegramPage.vue'

const routes = [
  {
    path: "/",
    name: 'Home',
    component: Home,
  },
  {
    path: "/testpage",
    name: 'test',
    component: testPage,
  },
  {
    path: "/Telegrampage",
    name: 'Telegram',
    component: TelegramPage
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router
