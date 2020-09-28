<template>
  <LoadingControl :loading-state="loadingState">
    <div class="bg-white d-flex align-items-center justify-content-center flex-fill flex-column w-100 ">
      <div>
        <span class="counter">{{ totalFormatted }}</span>
        <span class="counter-trend" :class="getTrendClass()"></span>
      </div>
      <span class="subtitle text-center">Pageviews taz.de gesamt</span>
    </div>
  </LoadingControl>
</template>

<script lang="ts">
import Vue from 'vue'

import { getTimeframeById, Timeframe, TimeframeId } from '@/common/timeframe'
import { LoadingState } from '@/common/LoadingState'
import { ApiClient } from '@/client/ApiClient'

import LoadingControl from '@/components/LoadingControl.vue'
import { GlobalPulse, PULSE_EVENT } from '@/common/GlobalPulse'
import { getTrend } from '@/utils/trends'

let currentRequestController: AbortController | null = null
const apiClient = new ApiClient()

interface Data {
  loadingState: LoadingState;
  total: number;
  totalPrevious: number;
}

interface Methods {
  updateData (timeframe: Timeframe): void;
  getTrendClass (): string;
}

interface Computed {
  totalFormatted: string;
}

export default Vue.extend<Data, Methods, Computed, {}>({
  name: 'ClickCounter',
  components: {
    LoadingControl
  },
  data () {
    return {
      total: 0,
      totalPrevious: 0,
      loadingState: LoadingState.FRESH
    }
  },
  computed: {
    totalFormatted (): string {
      return this.total?.toLocaleString() ?? ''
    }
  },
  methods: {
    async updateData (timeframe: Timeframe) {
      this.loadingState = LoadingState.LOADING
      try {
        if (currentRequestController !== null) {
          currentRequestController.abort()
        }
        currentRequestController = new AbortController()
        const { signal } = currentRequestController!!
        const totalResponse = (await apiClient.total(timeframe.minDate(), timeframe.maxDate(), null, {
          signal
        }))
        this.total = totalResponse.total
        this.totalPrevious = totalResponse.total_previous
        currentRequestController = null
        this.loadingState = LoadingState.SUCCESS
      } catch (e) {
        if (!(e instanceof DOMException)) {
          this.loadingState = LoadingState.ERROR
        }
      }
    },
    getTrendClass () {
      const trend = getTrend(this.totalPrevious, this.total, true)
      const arrowType = trend.direction * trend.score
      return `tazboard-trend-${arrowType}`
    }
  },
  watch: {
    '$route.query': {
      handler (query: any, oldQuery: any) {
        if (query.timeframeId !== oldQuery?.timeframeId) {
          const timeframe = getTimeframeById(query.timeframeId)
          this.updateData(timeframe!!)
        }
      },
      immediate: true,
      deep: true
    }
  },
  mounted () {
    GlobalPulse.$on(PULSE_EVENT, () => {
      const timeframe = getTimeframeById(this.$route.query.timeframeId as TimeframeId)
      if (timeframe) {
        this.updateData(timeframe)
      }
    })
  }
})
</script>
<style lang="scss" scoped>
@import "src/style/variables";
@import "src/style/mixins";

.click-counter-card {
  box-shadow: #2c3e50;
  display: flex;
  align-items: center;
  justify-content: center;
}

.counter {
  @include serif-font();
  @include light-text-shadow();
  color: #7DD2D2;
  font-weight: bold;
  font-size: min(4vw, 4.5rem);
}

.subtitle {
  color: #5D5D5D;
  font-size: min(2vw, 2rem);
  font-weight: bold;
}

.counter-trend {
  font-size: min(4vw, 3rem);
  justify-content: center;
  padding: 10px;
}
</style>
