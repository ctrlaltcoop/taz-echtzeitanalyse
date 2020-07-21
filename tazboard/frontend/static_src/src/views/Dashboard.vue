<template>
  <div class="dashboard">
    <div class="container">
      <div class="banner row">
        <div class="col-6 col-lg-2 logo-container pr-0 pl-0">
          <img class="img-fluid" src="../assets/logo_taz.png" alt="logo">
        </div>
        <div class="col-6 col-lg-5 pr-0 app-heading-container">
          <h1 class="app-heading">die echtzeitanalyse</h1>
        </div>
        <div class="col-12 col-lg-5 pr-0 timeframe-select-area">
          <div class="timeframe-select-container">
            <span class="timeframe-caption">{{
                currentTimeframe.minDate.toLocaleString([], dateFormatOptions)
              }} - {{ currentTimeframe.maxDate.toLocaleString([], dateFormatOptions) }}</span>
            <select class="timeframe-select" @change="timeframeSelect($event.target.value)"
                    :value="currentTimeframe.id">
              <option v-for="timeframe in timeframeSelection" :value="timeframe.id" :key="timeframe.id">
                {{ timeframe.label }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <Statistics/>
      <div>
          <BTabs card>
            <template v-slot:tabs-end>
              <li class="nav-item">
                <router-link class="nav-link" active-class="active" to="/toplist">Artikel Top X</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/fireplace">Kamin</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/focusTopics">Schwerpunkte Top 10</router-link>
              </li>
            </template>
          </BTabs>
      </div>
      <router-view/>
    </div>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'
import { BTabs } from 'bootstrap-vue'
import Statistics from '@/components/Statistics.vue'
import { ActionTypes } from '@/store/dataset/types'
import store from '@/store'
import { DEFAULT_TIMEFRAME, getTimeframeById, Timeframe, TimeframeId, TIMEFRAMES } from '@/common/timeframe'

export default Vue.extend({
  name: 'Dashboard',
  components: {
    Statistics,
    BTabs
  },
  data () {
    return {
      timeframeSelection: TIMEFRAMES,
      dateFormatOptions: {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }
    }
  },
  computed: {
    currentTimeframe (): Timeframe {
      const currentTimeframeId = this.$route.query.timeframeId as TimeframeId
      const currentTimeframe = getTimeframeById(currentTimeframeId)
      if (!currentTimeframe) {
        this.timeframeSelect(DEFAULT_TIMEFRAME.id)
        return DEFAULT_TIMEFRAME
      } else {
        return currentTimeframe
      }
    }
  },
  methods: {
    timeframeSelect (timeframeId: TimeframeId) {
      if (timeframeId === this.$route.query.timeframeId as TimeframeId) {
        return
      }
      this.$router.push({
        path: this.$route.path,
        params: this.$route.params,
        query: {
          ...this.$route.query,
          timeframeId
        }
      })
    }
  }
})
</script>
<style lang="scss">
@import "../style/variables";

.app-heading {
  margin: 1.9rem 0 0 1rem;
  font-size: 3.5em;
  font-weight: bold;
}

.logo-container {
  display: flex;
}

.timeframe-select-area {
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;

  .timeframe-select-container {

  }

  .timeframe-select {
    /* reset */
    border: none;
    -moz-appearance: none;
    -webkit-appearance: none;
    appearance: none;
    background-color: transparent;

    margin-left: 0.4rem;
    color: $taz-red;
    font-size: 1.0em;
    font-weight: bold;
    background-repeat: no-repeat;
    background-position-x: 100%;
    background-position-y: 5px;
  }

  .timeframe-caption {
    font-weight: bold;
    font-size: 1.2em;
  }
}
</style>
