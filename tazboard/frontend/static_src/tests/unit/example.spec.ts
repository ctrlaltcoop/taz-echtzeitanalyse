import { createLocalVue, shallowMount } from '@vue/test-utils'
import Dashboard from '@/views/Dashboard.vue'
import VueRouter from 'vue-router'
import Vue from 'vue'

describe('Dashboard.vue', () => {
  let router: VueRouter
  let localVue: typeof Vue
  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(VueRouter)
    router = new VueRouter()
  })
  it('renders props.msg when passed', () => {
    router = new VueRouter()
    const wrapper = shallowMount(Dashboard, {
      localVue,
      router
    })
    expect(wrapper.text()).toContain('die echtzeitanalyse')
  })
})
