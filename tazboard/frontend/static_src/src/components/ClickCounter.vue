<template>
  <LoadingControl :loading-state="loadingState">
    <div class="w-100 h-100 bg-white d-flex align-items-center justify-content-center flex-fill">
      <span class="counter">{{ total }}</span>
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

let currentRequestController: AbortController | null = null
const apiClient = new ApiClient()

interface Data {
  loadingState: LoadingState;
  total: number | null;
}

interface Methods {
  updateData (timeframe: Timeframe): void;
}

export default Vue.extend<Data, Methods, {}, {}>({
  name: 'ClickCounter',
  components: {
    LoadingControl
  },
  data () {
    return {
      total: null,
      loadingState: LoadingState.FRESH
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
        this.total = (await apiClient.total(timeframe.minDate(), timeframe.maxDate(), null, {
          signal
        })).total
        currentRequestController = null
        this.loadingState = LoadingState.SUCCESS
      } catch (e) {
        if (!(e instanceof DOMException)) {
          this.loadingState = LoadingState.ERROR
        }
      }
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

.click-counter-card {
  box-shadow: #2c3e50;
  display: flex;
  align-items: center;
  justify-content: center;
}

.counter {
  color: #7DD2D2;
  font-weight: bold;
  font-size: 4rem;
}
</style>
