import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Toplist from '@/views/Toplist.vue'
import Fireplace from '@/views/Fireplace.vue'
import FocusTopics from '@/views/FocusTopics.vue'

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
      },
      {
        path: '/fireplace',
        name: 'fireplace',
        component: Fireplace
      },
      {
        path: '/focusTopics',
        name: 'focus',
        component: FocusTopics
      }
    ]
  }
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
})

export default router
