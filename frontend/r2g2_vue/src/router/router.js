import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
import testPage from '../components/testPage.vue'
import TelegramPage from '../components/TelegramPage.vue'
import Page2 from '../components/Page2.vue'
import Page3 from '../components/Page3.vue'

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
  },
  {
    path: "/Page2",
    name: 'Page2',
    component: Page2
  },
  {
    path: "/Page3",
    name: 'Page3',
    component: Page3
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router
