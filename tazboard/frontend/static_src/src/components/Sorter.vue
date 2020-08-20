<template>
  <div class="sorter">
    <div class="caret-down" @click="$emit('descending')" :class="{ 'active': state === SortState.DESCENDING }"></div>
    <div class="caret-up" @click="$emit('ascending')" :class="{ 'active': state === SortState.ASCENDING }"></div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export enum SortState {
  ASCENDING, DESCENDING, NONE
}

interface Data {
  SortState: typeof SortState;
}

interface Props {
  state: SortState;
}

export default Vue.extend<Data, {}, {}, Props>({
  name: 'Sorter',
  props: {
    state: Number
  },
  data () {
    return {
      SortState
    }
  }
})
</script>
<style lang="scss" scoped>
@import "../style/variables";
@import "../style/arrows";

$caret-size: 25px;

.caret-up {
  @include arrow-up($caret-size, $gray-600);

  &.active {
    @include arrow-up($caret-size, $gray-700);
  }
}

.caret-down {
  @include arrow-down($caret-size, $gray-600);

  &.active {
    @include arrow-down($caret-size, $gray-700);
  }
}
</style>
