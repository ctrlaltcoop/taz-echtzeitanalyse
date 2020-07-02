<template>
  <div class="click-counter-card d-flex w-100 h-100">
    <span class="counter">{{ total }}</span>
  </div>
</template>

<script>

import { mapState } from 'vuex'

export default {
  name: 'ClickCounter',
  components: {},
  computed: {
    ...mapState({
      total: (state) => state.dataset?.current?.referrers?.total
    })
  }
}
</script>
<style lang="scss" scoped>
@import "src/style/variables";

.click-counter-card {
  background: $white;
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
