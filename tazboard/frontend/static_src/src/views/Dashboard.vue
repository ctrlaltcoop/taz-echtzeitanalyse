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
            <span class="pulse-caption">Letzte Aktualisierung: {{
                lastPulse.toLocaleString([], dateFormatOptions)
              }}</span>
            <span class="timeframe-caption">{{
                currentTimeframe.minDate().toLocaleString([], dateFormatOptions)
              }} - {{ currentTimeframe.maxDate().toLocaleString([], dateFormatOptions) }}</span>
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
      <div class="row">
        <BNav>
          <BNavItem v-for="tab in tabs" role="presentation" :to="tab.route" active-class="active"
                    :style="getTabStyleFor(tab)" :key="tab.route">
            <span class="tab-title-primary">{{ tab.primaryTitle }}</span><span class="tab-title-secondary"> {{ tab.secondaryTitle }}</span>
          </BNavItem>
        </BNav>
      </div>
      <div class="row content">
        <router-view/>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'
import { BNav, BNavItem } from 'bootstrap-vue'
import Statistics from '@/components/Statistics.vue'
import { DEFAULT_TIMEFRAME, getTimeframeById, Timeframe, TimeframeId, TIMEFRAMES } from '@/common/timeframe'
import { GlobalPulse, PULSE_EVENT, RESET_PULSE_EVENT } from '@/common/GlobalPulse'

interface TabConfig {
  route: string;
  order: number;
  primaryTitle: string;
  secondaryTitle: string;
}

const TABS: TabConfig[] = [
  {
    route: '/toplist',
    order: 0,
    primaryTitle: 'Artikel',
    secondaryTitle: 'Top 100'
  },
  {
    route: '/fireplace',
    order: 1,
    primaryTitle: 'Kamin',
    secondaryTitle: 'Top 10'
  },
  {
    route: '/subjects',
    order: 2,
    primaryTitle: 'Schwerpunkte',
    secondaryTitle: 'Top 10'
  }
]

export default Vue.extend({
  name: 'Dashboard',
  components: {
    Statistics,
    BNavItem,
    BNav
  },
  data () {
    return {
      tabs: TABS,
      lastPulse: new Date(),
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
  mounted () {
    GlobalPulse.$on(PULSE_EVENT, (date: Date) => {
      this.lastPulse = date
    })
    GlobalPulse.$on(RESET_PULSE_EVENT, (date: Date) => {
      this.lastPulse = date
    })
  },
  methods: {
    getTabStyleFor (tab: TabConfig) {
      const maxOrder = Math.max(...TABS.map(({ order }) => order))
      const zBoost = this.$route.path === tab.route ? maxOrder : 0
      return {
        'z-index': maxOrder - tab.order + zBoost
      }
    },
    timeframeSelect (timeframeId: TimeframeId) {
      if (timeframeId === this.$route.query.timeframeId as TimeframeId) {
        return
      }
      GlobalPulse.$emit(RESET_PULSE_EVENT, new Date())
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
<style lang="scss" scoped>
@import "../style/variables";

.nav {
  border: none;

  .nav-link {
    padding: 0.5rem 3rem;
    font-size: 1.5rem;
    font-weight: bold;
    background: $taz-red-light;
    border: none;
    border-top-left-radius: 0.75em;
    border-top-right-radius: 0.75em;
    position: relative;
    box-shadow: 0 0 6px 0 rgba(0,0,0,0.75);
    &.active {
      background-color: $taz-red;
    }
  }
}

.tab-title-primary {
  color: $white;
}

.tab-title-secondary {
  color: $black;
}

.app-heading {
  margin: 1.9rem 0 0 1rem;
  font-size: 3.5em;
  font-weight: bold;
}

.content {
  z-index: 21;
  position: relative;
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

  .pulse-caption {
    display: flex;
  }

  .timeframe-caption {
    font-weight: bold;
    font-size: 1.2em;
  }
}
</style>
