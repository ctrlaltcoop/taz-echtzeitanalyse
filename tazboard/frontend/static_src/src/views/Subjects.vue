<template>
  <LoadingControl class="loading-control" :loading-state="loadingState">
    <BTable
      striped
      class="w-100"
      :fields="fields"
      :items="items"
      :tbody-transition-props="{ name: 'statistics-table' }"
      v-model="rowItems"
      thead-class="table-head">
      <template v-slot:head(referrerSelect)="data">
        <div class="stacked-th-with-selection">
          <div>{{ data.label }}</div>
          <select class="referrer-select" v-model="selectedReferrer">
            <option v-for="referrer in availableReferrers" :value="referrer" :key="referrer">
              {{ referrer }}
            </option>
          </select>
        </div>
      </template>

      <template v-slot:cell(subject_name)="row">
        <span class="row-subjectName" @click="toggleDetails(row)">
          {{ row.item.subject_name }}
        </span>
      </template>

      <template v-slot:row-details="row">
        <SubjectRowDetail :item="row.item"/>
      </template>
    </BTable>
  </LoadingControl>
</template>

<script lang="ts">
import Vue from 'vue'
import { BTable } from 'bootstrap-vue'

import { getTimeframeById, Timeframe, TimeframeId } from '@/common/timeframe'
import LoadingControl from '@/components/LoadingControl.vue'
import { LoadingState } from '@/common/LoadingState'
import { GlobalPulse, PULSE_EVENT } from '@/common/GlobalPulse'
import { SubjectsData } from '@/dto/SubjectsDto'
import { ApiClient } from '@/client/ApiClient'
import SubjectRowDetail from '@/components/SubjectRowDetail'

const apiClient = new ApiClient()

interface Data {
  items: SubjectsData[];
  selectedReferrer: string | null;
  rowItems: Array<any>;
  loadingState: LoadingState;
}

interface Methods {
  loadData (timeframe: Timeframe): Promise<void>;
  fetchData (timeframe: Timeframe, signal: AbortSignal): Promise<void>;
  toggleDetails (row: any): void;
  syncOpenedDetailsStateWithRoute (): void;
  formatSelectReferrer (value: null, key: string, item: SubjectsData): string | undefined;
}

interface Computed {
  availableReferrers: Array<string>;
  openSubjects: Array<string>;
}

let currentRequestController: AbortController | null = null

export default Vue.extend<Data, Methods, Computed, {}>({
  name: 'Subjects',
  components: {
    SubjectRowDetail,
    BTable,
    LoadingControl
  },
  methods: {
    toggleDetails (row: any) {
      const query = this.$route.query.openSubjects as string || '[]'
      let currentlyOpenSubjects = JSON.parse(query)
      if (currentlyOpenSubjects.includes(row.item.subject_name)) {
        currentlyOpenSubjects = currentlyOpenSubjects.filter(
          (subjectName: string) => subjectName !== row.item.subject_name
        )
      } else {
        currentlyOpenSubjects.push(row.item.subject_name)
      }
      this.$router.push({
        path: this.$route.path,
        params: this.$route.params,
        query: {
          ...this.$route.query,
          openSubjects: JSON.stringify(currentlyOpenSubjects)
        }
      })
    },
    syncOpenedDetailsStateWithRoute () {
      for (const row of this.rowItems) {
        if (this.openSubjects.includes(row.subject_name)) {
          this.$set(row, '_showDetails', true)
        } else {
          this.$set(row, '_showDetails', false)
        }
      }
    },
    async loadData (timeframe: Timeframe) {
      this.loadingState = LoadingState.LOADING
      try {
        if (currentRequestController !== null) {
          currentRequestController.abort()
        }
        currentRequestController = new AbortController()
        const { signal } = currentRequestController!!
        // @ts-ignore abstract functions in vue components not supported which leads to broken type inference
        await this.fetchData(timeframe, signal)
        currentRequestController = null
        this.loadingState = LoadingState.SUCCESS
      } catch (e) {
        if (!(e instanceof DOMException)) {
          this.loadingState = LoadingState.ERROR
        }
      }
    },
    async fetchData (timeframe: Timeframe, signal: AbortSignal) {
      this.items = (await apiClient.subjects(timeframe.minDate(), timeframe.maxDate(), 10, { signal })).data
    },
    formatSelectReferrer (value: null, key: string, item: SubjectsData): string | undefined {
      if (this.selectedReferrer === null) {
        this.selectedReferrer = item.referrers[0].referrer
      }
      const selectedReferrer = this.selectedReferrer
      return item.referrers.find(({ referrer }) => {
        return selectedReferrer === referrer
      })?.percentage.toLocaleString([], { style: 'percent' })
    }
  },
  computed: {
    availableReferrers () {
      const allReferrers = this.items.map((item) => {
        return item.referrers.map((referrer) => referrer.referrer)
      }).flat()
      return [...new Set(allReferrers)]
    },
    openSubjects () {
      return JSON.parse(this.$route.query.openSubjects as string || '[]')
    }
  },
  data () {
    return {
      rowItems: [],
      selectedReferrer: null,
      loadingStateTimeframe: LoadingState.FRESH,
      fields: [
        {
          key: 'hits',
          label: 'Pageviews',
          class: 'text-right',
          thClass: 'taztable-th',
          formatter: (value: number) => value.toLocaleString(),
          sortable: true
        },
        {
          key: 'subject_name',
          label: 'Schwerpunkt',
          class: 'text-left',
          thClass: 'taztable-th'
        },
        {
          key: 'article_count',
          label: 'Artikelanzahl',
          class: 'text-left',
          thClass: 'taztable-th',
          sortable: true
        },
        {
          key: 'referrerSelect',
          label: 'Klicks über',
          class: 'text-right',
          thClass: 'taztable-th',
          formatter: (value: null, key: string, item: SubjectsData) => {
            // @ts-ignore type inference of this doesn't work here
            return this.formatSelectReferrer(value, key, item)
          }
        }
      ],
      items: [],
      loadingState: LoadingState.FRESH
    }
  },
  watch: {
    rowItems () {
      this.syncOpenedDetailsStateWithRoute()
    },
    '$route.query': {
      handler (query: any, oldQuery: any) {
        if (query.timeframeId !== oldQuery?.timeframeId) {
          const timeframe = getTimeframeById(query.timeframeId)
          this.loadData(timeframe!!)
        }
        this.syncOpenedDetailsStateWithRoute()
      },
      immediate: true,
      deep: true
    }
  },
  mounted () {
    GlobalPulse.$on(PULSE_EVENT, () => {
      const timeframe = getTimeframeById(this.$route.query.timeframeId as TimeframeId)
      if (timeframe) {
        this.loadData(timeframe!!)
      }
    })
  }
})
</script>

<!-- styles for vue table won't take effect unless unscoped -->
<style lang="scss">
@import 'src/style/variables';

.row-subjectName {
  font-size: 1.4rem;
  font-weight: bold;
  display: block;
}

.row-headline-kicker {
  font-size: 1rem;
  display: block;
  color: $gray-700;
}

.table-head {
  background-color: $taz-red;

}

.taztable-th {
  color: $white;
  font-size: 2rem;
  // found no different way to overwrite default style
  border-top: none !important;
}
</style>

<style lang="scss" scoped>
.loading-control {
  min-height: 450px;
  flex-direction: column;
}

.table {
  th {
    border: none;
  }
}

</style>
