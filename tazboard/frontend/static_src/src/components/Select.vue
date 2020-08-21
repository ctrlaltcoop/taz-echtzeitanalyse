<template>
  <div class="select-wrapper" :style="selectStyle">
    <select ref="select" @input="updateStyle(); $emit('input', $event.target.value)"
            :value="value">
      <option v-for="item in items" :value="getValue(item)" :key="getKey(item)">
        {{ getLabel(item) }}
      </option>
    </select>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

interface Props {
  value: string;
  valueProperty: string | undefined;
  labelProperty: string | undefined;
  keyProperty: string | undefined;
  items: Array<object | string>;
  autoWidth: boolean;
}

export default Vue.extend<{}, {}, {}, Props>({
  name: 'Select',
  props: {
    value: String,
    valueProperty: {
      type: String,
      required: false
    },
    labelProperty: {
      type: String,
      required: false
    },
    keyProperty: {
      type: String,
      required: false
    },
    items: Array,
    autoWidth: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      selectStyle: {}
    }
  },
  methods: {
    getLabel (item) {
      if (this.labelProperty) {
        return item[this.labelProperty]
      } else {
        return item
      }
    },
    getValue (item) {
      if (this.valueProperty) {
        return item[this.valueProperty]
      } else {
        return item
      }
    },
    getKey (item) {
      if (this.keyProperty) {
        return item[this.keyProperty]
      } else {
        return item
      }
    },
    updateStyle () {
      if (this.$refs.select && this.autoWidth) {
        const textNode = Array.from(this.$refs.select.children).find((option: HTMLOptionElement) => option.selected) as Node
        if (textNode) {
          const range = document.createRange()
          range.selectNodeContents(textNode)
          let optionWidth = range.getClientRects()?.[0]?.width
          if (optionWidth) {
            // add a little padding on the right so it doesn't look cut-off
            optionWidth += 25
          }
          this.selectStyle = {
            width: `${optionWidth ?? this.$refs.select.clientWidth}px`
          }
        }
      }
    }
  },
  mounted () {
    Vue.nextTick(() => this.updateStyle())
  }
})
</script>
<style lang="scss" scoped>
@import "../style/variables";

.select-wrapper {
  display: flex;
  cursor: default;
  position: relative;

  &:after {
    position: absolute;
    right: 0;
    top: 0.6rem;
    line-height: 0;
    font-family: icons, fantasy;
    content: '\e900';
  }
}

select {
  width: 100%;
  z-index: 99;
  border: none;
  padding-right: 10px;
  -moz-appearance: none;
  -webkit-appearance: none;
  appearance: none;
  background-color: transparent;
  font-size: 1.0rem;
  font-weight: bold;
  color: inherit;

  option {
    color: inherit;
  }
}

</style>
