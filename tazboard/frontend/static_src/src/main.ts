import Vue from 'vue'
import App from './App.vue'
import store from '@/store'
import router from './router'
import 'chart.js'
import 'chartjs-adapter-date-fns'

import '@/style/main.scss'

if (process.env.VUE_APP_MOCK_ENABLED) {
  require('../tests/mocks/install')
}

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
