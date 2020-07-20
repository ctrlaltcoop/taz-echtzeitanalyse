<template>
  <LoadingControl :loading-state="loadingState">
    <div class="w-100 h-100 bg-white d-flex align-items-center justify-content-center flex-fill">
      <span class="counter">{{ total }}</span>
    </div>
  </LoadingControl>
</template>

<script lang="ts">
import Vue from 'vue'

import { getTimeframeById, Timeframe } from '@/common/timeframe'
import { LoadingState } from '@/common/LoadingState'
import { ApiClient } from '@/client/ApiClient'

import LoadingControl from '@/components/LoadingControl.vue'

let currentRequestController: AbortController | null = null
const apiClient = new ApiClient()

interface Data {
  loadingState: LoadingState;
  total: number | null;
}

interface Methods {
  update (timeframe: Timeframe): void;
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
    async update (timeframe: Timeframe) {
      this.loadingState = LoadingState.LOADING
      try {
        if (currentRequestController !== null) {
          currentRequestController.abort()
        }
        currentRequestController = new AbortController()
        const { signal } = currentRequestController!!
        this.total = (await apiClient.total(timeframe.minDate, timeframe.maxDate, null, {
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
          this.update(timeframe!!)
        }
      },
      immediate: true,
      deep: true
    }
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
