<template>
  <div class="row statistics-area">
    <div class="col-4 pt-5 pb-5  statistics-ticker">
      <Ticker class="card-shadow" />
    </div>
    <div class="col-4 pt-5 pb-5 statistics-stats">
        <div class="col-6 p-0 click-counter-area">
          <ClickCounter class="card-shadow" />
        </div>
    </div>
    <div class="col-4 pt-5 pb-5 statistics-referrer">
      <ReferrerDevices class="card-shadow" />
    </div>
  </div>
</template>

<script lang="ts">
import Ticker from '@/components/Ticker.vue'
import ClickCounter from '@/components/ClickCounter.vue'
import ReferrerDevices from '@/components/ReferrerDevices.vue'

export default {
  name: 'Statistics',
  components: {
    ClickCounter,
    Ticker,
    ReferrerDevices
  }
}
</script>
<style lang="scss">
@import "src/style/variables";

.statistics-area {
  background: $gray-200;
}

.statistics-ticker {
  height: 300px;
  display: flex;
}

.statistics-referrer {
  height: 300px;
  display: flex;
}

.statistics-stats {
  height: 300px;
  display: flex;
}

.click-counter-area {
  display: flex;
}

</style>
