import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
import TelegramPage from '../components/TelegramPage.vue'
import Page2 from '../components/Page2.vue'

const routes = [
  {
    path: "/",
    name: 'Home',
    component: Home,
  },
  {
    path: "/Telegrampage",
    name: 'Telegram',
    component: TelegramPage
  },
  {
    path: "/Page2",
    name: 'Page2',
    component: Page2
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router
