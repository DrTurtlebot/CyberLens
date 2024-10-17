import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/pages/MainApp.vue';  // Import your Home component
import About from '../components/pages/About.vue';
import BugReport from '../components/pages/BugReport.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home, // Use the Home component
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
  history: createWebHistory(),  // Use HTML5 history mode for clean URLs
  routes,
});

export default router;
