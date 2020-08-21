<template>
  <div class="d-flex w-100 h-100 tazboard-shimmer-wrapper" :class="{
    'loading-control-error': loadingState === LoadingState.ERROR,
    'loading-control-success': loadingState === LoadingState.SUCCESS,
    'loading-control-loading': loadingState === LoadingState.LOADING,
  }">
    <div class="h-100 w-100 flex-fill failed d-flex align-items-center flex-column justify-content-center" v-if="loadingState === LoadingState.ERROR">
      <img src="../assets/ikons/cloud_fail.svg">
      <span>Fehler bei der Verbindung zum Server</span>
    </div>
    <div class="h-100 w-100 tazboard-shimmer-animate" v-if="loadingState === LoadingState.LOADING"/>
    <slot v-if="loadingState === LoadingState.SUCCESS"/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { LoadingState } from '@/common/LoadingState'

interface Props {
  loadingState: LoadingState;
}

interface Data {
  LoadingState: typeof LoadingState;
}

export default Vue.extend<Data, {}, {}, Props>({
  name: 'LoadingControl',
  props: {
    loadingState: Number
  },
  data: () => {
    return {
      LoadingState: LoadingState
    }
  }
})
</script>
<style lang="scss" scoped>
@import "../style/variables";
.failed {
  background: $gray-500;
}
</style>
