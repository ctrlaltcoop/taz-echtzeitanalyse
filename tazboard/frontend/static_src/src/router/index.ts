import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Toplist from '@/views/Toplist.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    component: Dashboard,
    children: [
      {
        path: '',
        redirect: '/toplist'
      },
      {
        path: '/toplist',
        name: 'toplist',
        component: Toplist
      }
    ]
  }
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
})

export default router
