import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
import testPage from '../components/testPage.vue'

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
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router
