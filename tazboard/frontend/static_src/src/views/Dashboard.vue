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
                currentTimeframe.start().toLocaleString([], dateFormatOptions)
              }} - {{ currentTimeframe.end().toLocaleString([], dateFormatOptions) }}</span>
            <select class="timeframe-select" @change="timeframeSelect($event.target.value)"
                    :value="currentTimeframe.minDate">
              <option v-for="timeframe in timeframeSelection" :value="timeframe.minDate" :key="timeframe.minDate">
                {{ timeframe.label }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <Statistics/>
      <router-view/>
    </div>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'
import { subDays, subMinutes, subMonths } from 'date-fns'
import Statistics from '@/components/Statistics.vue'
import { ActionTypes } from '@/store/dataset/types'
import store from '@/store'

interface Timeframe {
  label: string;
  start: () => Date;
  end: () => Date;
  minDate: string;
}

async function updateTimeframeHistogram (minDate: string) {
  await store.dispatch(ActionTypes.SET_TIMEFRAME, {
    min: minDate,
    max: 'now'
  })
}

export default Vue.extend({
  name: 'Dashboard',
  data () {
    return {
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
    timeframeSelection (): Array<Timeframe> {
      return [{
        label: '10 minuten',
        start: () => subMinutes(new Date(), 5),
        end: () => new Date(),
        minDate: 'now-10m'
      }, {
        label: 'Heute',
        start: () => subDays(new Date(), 1
        ),
        end: () => new Date(),
        minDate: 'now-24h'
      }, {
        label: '1 Monat',
        start: () => subMonths(new Date(), 1),
        end: () => new Date(),
        minDate: 'now-1M'
      }]
    },
    currentTimeframe (): Timeframe {
      const currentQuery = this.$route.query.minDate
      const currentTimeframe = this.timeframeSelection.find(({ minDate }) => minDate === currentQuery)
      if (!currentTimeframe) {
        this.timeframeSelect(this.timeframeSelection[0].minDate)
        return this.timeframeSelection[0]
      } else {
        return currentTimeframe
      }
    }
  },
  components: {
    Statistics
  },
  methods: {
    timeframeSelect (minDate: string) {
      if (minDate === this.$route.query.minDate) {
        return
      }
      this.$router.push({
        path: this.$route.path,
        params: this.$route.params,
        query: {
          ...this.$route.query,
          minDate: minDate
        }
      })
    }
  },
  watch: {
    '$route.query': {
      handler: (query) => {
        if (query.minDate) {
          updateTimeframeHistogram(query.minDate as string)
        }
      },
      immediate: true,
      deep: true
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
