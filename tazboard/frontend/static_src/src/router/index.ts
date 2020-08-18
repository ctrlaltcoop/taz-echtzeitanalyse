import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Toplist from '@/views/Toplist.ts'
import Fireplace from '@/views/Fireplace.ts'
import Subjects from '@/views/Subjects.vue'

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
        path: '/subjects',
        name: 'subjects',
        component: Subjects
      }
    ],
    meta: {
      title: 'die echtzeitanalyse'
    }
  }
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
})

export default router
