import Vue from 'vue'
import { DEFAULT_REFERRER_SELECT } from '@/common/constants'

interface Methods {
  selectReferrer (referrer: string): void;
}

interface Computed {
  selectedReferrer: string | null;
}

export const SelectReferrerMixin = Vue.extend<{}, Methods, Computed, {}>({
  methods: {
    selectReferrer (referrer: string) {
      this.$router.push({
        path: this.$route.path,
        params: this.$route.params,
        query: {
          ...this.$route.query,
          selectedReferrer: referrer
        }
      })
    }
  },
  computed: {
    selectedReferrer (): string | null {
      if (!this.$route.query.selectedReferrer) {
        this.selectReferrer(DEFAULT_REFERRER_SELECT)
        return DEFAULT_REFERRER_SELECT
      } else {
        return this.$route.query.selectedReferrer as string | null
      }
    }
  }
})
