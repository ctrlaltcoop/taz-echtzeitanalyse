<template>
  <LoadingControl class="tazboard-dashboard-table-loading-control" :loading-state="loadingState">
    <BTable
      striped
      class="w-100 tazboard-dashboard-table"
      :fields="fields"
      :items="items"
      :tbody-transition-props="{ name: 'statistics-table' }"
      v-model="rowItems"
      thead-class="tazboard-dashboard-table-head">

      <template v-slot:cell(index)="data">
        {{ data.index + 1 }}.
      </template>

      <template v-slot:head(referrerSelect)="data">
        <div class="tazboard-dashboard-table-th-stacked-with-selection">
          <div>{{ data.label }}</div>
          <Select @click="$event.stopPropagation()" class="tazboard-dashboard-table-referrer-select"
                  :items="availableReferrers"
                  @input="selectReferrer($event)" :value="selectedReferrer" :auto-width="true"/>
        </div>
      </template>

      <template v-slot:cell(subject_name)="row">
        <span class="row-subject" @click="toggleDetails(row)">
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
import SubjectRowDetail from '@/components/SubjectRowDetail.vue'
import Select from '@/components/Select.vue'
import { SelectReferrerMixin } from '@/common/SelectReferrerMixin'
import { CONNECTION_ALERT_EVENT, ConnectionAlertBus } from '@/common/ConnectionAlertBus'

const apiClient = new ApiClient()

interface Data {
  items: SubjectsData[];
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
    LoadingControl,
    Select
  },
  mixins: [SelectReferrerMixin],
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
      this.loadingState = this.loadingState !== LoadingState.SUCCESS ? LoadingState.LOADING : LoadingState.UPDATING
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
          if (this.loadingState === LoadingState.UPDATING) {
            ConnectionAlertBus.$emit(CONNECTION_ALERT_EVENT)
          } else {
            this.loadingState = LoadingState.ERROR
          }
        }
      }
    },
    async fetchData (timeframe: Timeframe, signal: AbortSignal) {
      this.items = (await apiClient.subjects(timeframe.minDate(), timeframe.maxDate(), 10, { signal })).data
    },
    formatSelectReferrer (value: null, key: string, item: SubjectsData): string | undefined {
      const referrer = item.referrers.find(({ referrer }) => {
        // @ts-ignore selectedReferrer is defined on mixin type inferrence fails
        return this.selectedReferrer === referrer
      })
      if (referrer) {
        return (`${referrer.hits.toString()} (${referrer.percentage.toLocaleString([], { style: 'percent' })})`)
      } else {
        return ''
      }
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
      fields: [
        {
          key: 'index',
          label: '#',
          tdClass: 'text-center tazboard-dashboard-table-td-hits align-middle',
          thClass: 'tazboard-dashboard-table-th text-center'
        },
        {
          key: 'hits',
          label: 'Pageviews',
          tdClass: 'text-right tazboard-dashboard-table-td-hits align-middle',
          thClass: 'tazboard-dashboard-table-th text-center',
          formatter: (value: number) => value.toLocaleString(),
          sortable: true
        },
        {
          key: 'subject_name',
          label: 'Schwerpunkt',
          tdClass: 'text-left align-middle',
          thClass: 'tazboard-dashboard-table-th tazboard-dashboard-table-th-title text-left'
        },
        {
          key: 'article_count',
          label: 'Artikelanzahl',
          tdClass: 'text-center align-middle',
          thClass: 'tazboard-dashboard-table-th text-center',
          sortable: true
        },
        {
          key: 'referrerSelect',
          label: 'Klicks über',
          tdClass: 'tazboard-dashboard-table-td-referrer-select align-middle text-right',
          thClass: 'tazboard-dashboard-table-th tazboard-dashboard-table-th-referrer-select tazboard-dashboard-table-th-black text-center',
          sortable: true,
          sortByFormatted: true,
          formatter: (value: null, key: string, item: SubjectsData) => {
            // @ts-ignore type inference of this doesn't work here
            return this.formatSelectReferrer(value, key, item)
          }
        }
      ],
      items: [],
      loadingState: LoadingState.FRESH as LoadingState
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
<style lang="scss" scoped>
@import 'src/style/variables';
@import "src/style/mixins";

.row-subject {
  @include serif-font;
  font-size: 1.4rem;
  font-weight: bold;
  display: block;
}

</style>
