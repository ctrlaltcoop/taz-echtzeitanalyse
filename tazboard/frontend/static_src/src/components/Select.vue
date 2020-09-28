<template>
  <div class="select-wrapper" :style="selectStyle">
    <select ref="select" @change="updateStyle(); $emit('input', $event.target.value)"
            :value="value">
      <option v-for="item in items" :value="getValue(item)" :key="getKey(item)" @click="$event.stopPropagation()">
        {{ getLabel(item) }}
      </option>
    </select>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { isObject } from '@/utils/objects'

type AnyObject = { [key: string]: any }

interface Data {
  selectStyle: object;
}

interface Props {
  value: string;
  valueProperty: string | undefined;
  labelProperty: string | undefined;
  keyProperty: string | undefined;
  items: Array<AnyObject | string>;
  autoWidth: boolean;
}

interface Methods {
  getLabel(item: object | string): string;
  getKey(item: object | string): string;
  getValue(item: object | string): string;
  updateStyle(): void;
}

export default Vue.extend<Data, Methods, {}, Props>({
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
    getLabel (item: AnyObject | string) {
      if (this.labelProperty && isObject(item)) {
        return item[this.labelProperty]
      } else {
        return item
      }
    },
    getValue (item: AnyObject | string) {
      if (this.valueProperty && isObject(item)) {
        return item[this.valueProperty]
      } else {
        return item
      }
    },
    getKey (item: AnyObject | string) {
      if (this.keyProperty && isObject(item)) {
        return item[this.keyProperty]
      } else {
        return item
      }
    },
    updateStyle () {
      if (this.$refs.select instanceof Element && this.autoWidth) {
        const select = this.$refs.select
        // @ts-ignore typescript complains although Array.from(HTMLOptionElement[]) is perfectly OK
        const textNode = Array.from(select.children as HTMLOptionElement[])
          .find((option: HTMLOptionElement) => option.selected) as HTMLOptionElement
        if (textNode) {
          const range = document.createRange()
          range.selectNodeContents(textNode)
          let optionWidth = range.getClientRects()?.[0]?.width
          if (optionWidth) {
            // add a little padding on the right so it doesn't look cut-off
            optionWidth += 25
          }
          this.selectStyle = {
            width: `${optionWidth ?? select.clientWidth}px`
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
    color: initial;
  }

}

</style>
