import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
import newsPage from '../components/newsPage.vue'

const routes = [
  {
    path: "/",
    name: 'Home',
    component: Home,
  },
  {
    path: "/newspage",
    name: 'news',
    component: newsPage,
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router
