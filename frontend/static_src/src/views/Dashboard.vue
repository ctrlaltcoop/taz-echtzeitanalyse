<template>
  <div class="dashboard">
    <div class="container">
      <div class="banner row">
        <div class="col-6 col-lg-2 logo-container pl-0 pr-0" >
          <img class="img-fluid" src="../assets/logo_taz.png" alt="logo">
        </div>
        <div class="col-6 col-lg-5 pr-0 pl-0 app-heading-container">
          <h1 class="app-heading">die echtzeitanalyse</h1>
        </div>
        <div class="col-12 col-lg-5 pr-0 timeframe-select-area">
          <div class="timeframe-select-container">
            <span class="timeframe-caption">{{ currentTimeframe.start().toLocaleString([], dateFormatOptions) }} - {{ currentTimeframe.end().toLocaleString([], dateFormatOptions) }}</span>
            <select class="timeframe-select" @change="timeframeSelect" :value="currentTimeframe.id">
              <option v-for="timeframe in timeframeSelection" :value="timeframe.id" :key="timeframe.id">{{ timeframe.label }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="ticker-area row">
        <Ticker/>
      </div>
      <router-view/>
    </div>
  </div>
</template>
<script lang="ts">
import Ticker from '@/components/Ticker.vue'
import Vue from 'vue'
import { subMinutes, subMonths } from 'date-fns'

enum TimeframeId {
  FIVE_MINUTES, TODAY, THREE_MONTHS
}

interface Timeframe {
  id: TimeframeId;
  label: string;
  start: () => Date;
  end: () => Date;
}

export default Vue.extend({
  name: 'Dashboard',
  data () {
    return {
      dateFormatOptions: { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    }
  },
  computed: {
    timeframeSelection (): Array<Timeframe> {
      return [{
        id: TimeframeId.FIVE_MINUTES,
        label: '5 minuten',
        start: () => subMinutes(new Date(), 5),
        end: () => new Date()
      }, {
        id: TimeframeId.TODAY,
        label: 'Heute',
        start: () => new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate()),
        end: () => new Date()
      }, {
        id: TimeframeId.THREE_MONTHS,
        label: '3 Monate',
        start: () => subMonths(new Date(), 3),
        end: () => new Date()
      }]
    },
    currentTimeframe (): Timeframe {
      const currentId = parseInt(this.$route.query.timeframe as string) || TimeframeId.FIVE_MINUTES
      return this.timeframeSelection.find(({ id }) => id === currentId as TimeframeId) as Timeframe
    }
  },
  components: {
    Ticker
  },
  methods: {
    timeframeSelect (event: Event) {
      const selectedTimeframeId = parseInt((event.target as HTMLInputElement)?.value) as TimeframeId
      this.$router.push({
        path: this.$route.path,
        params: this.$route.params,
        query: {
          ...this.$route.query,
          timeframe: selectedTimeframeId.toString()
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

.ticker-area {
  background: $gray-200;
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
    -moz-appearance:none;
    -webkit-appearance:none;
    appearance:none;
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
