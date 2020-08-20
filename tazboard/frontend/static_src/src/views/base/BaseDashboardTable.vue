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

      <template v-slot:cell(headline)="row">
        <span class="row-headline-kicker">
          {{ row.item.kicker }}
        </span>
        <span class="row-headline-headline" @click="toggleDetails(row)">
          {{ row.item.headline }}
        </span>
      </template>

      <template v-slot:cell(trend)="row">
        <span v-if="row.item.hits_previous === 0">
          Neu
        </span>
        <span v-else :class="getTrendClass(row.item)"></span>
      </template>

      <template v-slot:row-details="row">
        <ArticleRowDetail :item="row.item"/>
      </template>
    </BTable>
  </LoadingControl>
</template>

<script lang="ts">
import Vue from 'vue'
import { BTable } from 'bootstrap-vue'

import { ArticleData } from '@/dto/ToplistDto'
import { getTimeframeById, Timeframe, TimeframeId } from '@/common/timeframe'
import { TOP_REFERRER_THRESHOLD } from '@/common/constants'
import ArticleRowDetail from '@/components/ArticleRowDetail'
import LoadingControl from '@/components/LoadingControl.vue'
import { LoadingState } from '@/common/LoadingState'
import { GlobalPulse, PULSE_EVENT } from '@/common/GlobalPulse'
import { formatPublicationTime } from '@/utils/time'
import { getTrend } from '@/utils/trends'

interface Data {
  items: ArticleData[];
  selectedReferrer: string | null;
  rowItems: Array<any>;
  loadingState: LoadingState;
}

interface Methods {
  loadData (timeframe: Timeframe): Promise<void>;
  toggleDetails (row: any): void;
  syncOpenedDetailsStateWithRoute (): void;
  formatSelectReferrer (value: null, key: string, item: ArticleData): string | undefined;
  getTrendClass (item: ArticleData): string;
}

interface Computed {
  availableReferrers: Array<string>;
  openedMsids: Array<number>;
}

let currentRequestController: AbortController | null = null

export default Vue.extend<Data, Methods, Computed, {}>({
  name: 'BaseDashboardTable',
  components: {
    BTable,
    LoadingControl,
    ArticleRowDetail
  },
  methods: {
    toggleDetails (row: any) {
      const query = this.$route.query.openMsids as string || '[]'
      let currentlyOpenMsids = JSON.parse(query)
      if (currentlyOpenMsids.includes(row.item.msid)) {
        currentlyOpenMsids = currentlyOpenMsids.filter((msid: number) => msid !== row.item.msid)
      } else {
        currentlyOpenMsids.push(row.item.msid)
      }
      this.$router.push({
        path: this.$route.path,
        params: this.$route.params,
        query: {
          ...this.$route.query,
          openMsids: JSON.stringify(currentlyOpenMsids)
        }
      })
    },
    syncOpenedDetailsStateWithRoute () {
      for (const row of this.rowItems) {
        if (this.openedMsids.includes(row.msid)) {
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
    formatSelectReferrer (value: null, key: string, item: ArticleData): string | undefined {
      if (this.selectedReferrer === null) {
        this.selectedReferrer = item.referrers[0].referrer
      }
      const selectedReferrer = this.selectedReferrer
      return item.referrers.find(({ referrer }) => {
        return selectedReferrer === referrer
      })?.percentage.toLocaleString([], { style: 'percent' })
    },
    getTrendClass (item: ArticleData) {
      if (item.hits_previous === 0) {
        return ''
      } else {
        const trend = getTrend(item.hits_previous, item.hits, true)
        const arrowType = trend.direction * trend.score
        return `trend-${arrowType}`
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
    openedMsids () {
      return JSON.parse(this.$route.query.openMsids as string || '[]')
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
          tdClass: 'taztable-td-hits',
          formatter: (value: number) => value.toLocaleString(),
          sortable: true
        },
        {
          key: 'trend',
          label: '',
          class: 'text-center',
          thClass: 'taztable-th'
        },
        {
          key: 'headline',
          label: 'Titel',
          class: 'text-left',
          thClass: 'taztable-th'
        },
        {
          key: 'pubdate',
          label: 'veröffentlicht',
          class: 'text-right',
          thClass: 'taztable-th',
          formatter: formatPublicationTime,
          sortable: true
        }, {
          key: 'referrerSelect',
          label: 'Klicks über',
          class: 'text-right',
          thClass: 'taztable-th',
          formatter: (value: null, key: string, item: ArticleData) => {
            // @ts-ignore type inference of this doesn't work here
            return this.formatSelectReferrer(value, key, item)
          }
        }, {
          key: 'topReferrer',
          label: 'Top Referrer',
          class: 'text-right',
          thClass: 'taztable-th',
          formatter: (value: null, key: string, item: ArticleData) => {
            return item.referrers
              .filter(({ percentage }) => percentage > TOP_REFERRER_THRESHOLD)
              .map(({ referrer }) => referrer)
              .join(',')
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
@import "src/style/mixins";
@import 'src/style/variables';

.row-headline-headline {
  @include serif-font();
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

.taztable-td-hits {
  @include serif-font();
  @include light-text-shadow();
  font-weight: bold;
  font-size: 2rem;
  color: $gray-800;
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
