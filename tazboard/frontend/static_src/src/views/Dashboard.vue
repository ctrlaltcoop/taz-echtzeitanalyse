<template>
  <div class="dashboard">
    <ConnectionAlerter />
    <div class="container">
      <div class="banner row">
        <div class="col-6 col-lg-auto logo-container pr-0 pl-0">
          <img class="img-fluid" src="../assets/logo_taz.png" alt="logo">
        </div>
        <div class="col-6 col-lg-auto pt-2 pr-0 app-heading-container">
          <h1 class="app-heading">die echtzeitanalyse</h1>
          <a href="https://wiki.hal.taz.de/tazwiki/Echtzeit-Analyse">Was wird hier eigentlich gezählt?</a>
        </div>
        <div class="col-12 col-lg pr-0 timeframe-select-area">
            <span class="pulse-caption">Letzte Aktualisierung: {{
                lastPulse.toLocaleString([], dateFormatOptions)
              }}</span>
          <div class="d-flex">
            <span class="timeframe-caption">{{
                currentTimeframeOrDefault.minDate().toLocaleString([], dateFormatOptions)
              }} - {{ currentTimeframeOrDefault.maxDate().toLocaleString([], dateFormatOptions) }}</span>
            <Select
              class="tazboard-selection timeframe-select"
              @input="timeframeSelect($event)"
              :value="$route.query.timeframeId"
              :items="timeframeSelection"
              value-property="id"
              label-property="label"
              key-property="id"
            >
            </Select>
          </div>
        </div>
      </div>
      <Statistics/>
      <div class="row">
        <BNav>
          <BNavItem v-for="tab in tabs" role="presentation" :to="{
            path: tab.route,
            query: { timeframeId: $route.query.timeframeId }
          }" active-class="active"
                    :style="getTabStyleFor(tab)" :key="tab.route">
            <span class="tab-title-primary">{{ tab.primaryTitle }}</span><span
            class="tab-title-secondary"> {{ tab.secondaryTitle }}</span>
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
import {
  DEFAULT_TIMEFRAME,
  Timeframe,
  TimeframeId,
  TimeframeMixin,
  TIMEFRAMES
} from '@/common/timeframe'
import { GlobalPulse, PULSE_EVENT, RESET_PULSE_EVENT } from '@/common/GlobalPulse'
import Select from '@/components/Select.vue'
import ConnectionAlerter from '@/components/ConnectionAlerter.vue'

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
    primaryTitle: 'Startseite',
    secondaryTitle: 'Top 10'
  },
  {
    route: '/subjects',
    order: 2,
    primaryTitle: 'Schwerpunkte',
    secondaryTitle: 'Top 10'
  }
]

interface Data {
  tabs: Array<TabConfig>;
  lastPulse: Date;
  timeframeSelection: Array<Timeframe>;
  dateFormatOptions: { [key: string]: string };
}

interface Computed {
  currentTimeframeOrDefault: Timeframe;
}

interface Methods {
  getTabStyleFor (tab: TabConfig): { [key: string]: string | number };

  timeframeSelect (timeframeId: TimeframeId): void;
}

export default Vue.extend<Data, Methods, Computed, {}>({
  name: 'Dashboard',
  components: {
    Statistics,
    BNavItem,
    BNav,
    Select,
    ConnectionAlerter
  },
  mixins: [TimeframeMixin],
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
    currentTimeframeOrDefault (): Timeframe {
      // @ts-ignore typescript won't infer types from vue mixins unfortunately
      if (this.currentTimeframe == null) {
        this.timeframeSelect(DEFAULT_TIMEFRAME.id)
        return DEFAULT_TIMEFRAME
      } else {
        // @ts-ignore typescript won't infer types from vue mixins unfortunately
        return this.currentTimeframe
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
    getTabStyleFor (tab: TabConfig): { [key: string]: string | number } {
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
    box-shadow: 0 0 6px 0 rgba(0, 0, 0, 0.75);

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

.app-heading-container {
  display: flex;
  flex-direction: column;
}

.app-heading {
  font-weight: bold;
  margin: 0;
}

.content {
  z-index: 21;
  position: relative;
}

.logo-container {
  max-width: 170px;
}

.timeframe-select-area {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-end;

  .timeframe-select {
    color: $taz-red;
    margin-left: 0.4rem;
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
