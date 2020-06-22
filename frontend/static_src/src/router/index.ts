import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: Dashboard
  }
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
})

export default router
