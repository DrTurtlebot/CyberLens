import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/pages/MainApp.vue';
import About from '../components/pages/About.vue';
import BugReport from '../components/pages/BugReport.vue';

const routes = [
  {
    // NOTE: Add an optional parameter :searchParam?
    path: '/:searchParam?',
    name: 'Home',
    component: Home, 
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/bugreport',
    name: 'BugReport',
    component: BugReport,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;