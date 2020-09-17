<template>
  <LoadingControl class="tazboard-dashboard-table-loading-control" :loading-state="loadingState">
    <BTable
      striped
      class="w-100 tazboard-dashboard-table"
      :fields="fields"
      :items="items"
      tbody-tr-class="tazboard-dashboard-table-row"
      :tbody-transition-props="{ name: 'statistics-table' }"
      v-model="rowItems"
      thead-class="tazboard-dashboard-table-head"
      @row-clicked="toggleDetails">

      <template v-slot:cell(index)="data">
        {{ data.index + 1 }}.
      </template>

      <template v-slot:head(hits)="data">
        {{ data.label }}
      </template>

      <template v-slot:head(referrerSelect)="data">
        <div class="tazboard-dashboard-table-th-stacked-with-selection">
          <div>{{ data.label }}</div>
          <Select class="tazboard-dashboard-table-referrer-select" :items="availableReferrers"
                  @input="selectReferrer($event)" :value="selectedReferrer" :auto-width="true"/>
        </div>
      </template>

      <template v-slot:cell(headline)="row">
        <span class="tazboard-dashboard-table-row-headline-kicker">
          {{ row.item.kicker || '-' }}
        </span>
        <a
          target="_blank"
          :href="row.item.url" :alt="row.item.headline"
          class="tazboard-dashboard-table-row-headline-headline"
          @click="$event.stopPropagation()"
          :class="{
            'archive': row.item.archive,
            'frontpage': row.item.frontpage
          }">
          {{ row.item.headline }}
        </a>
      </template>

      <template v-slot:cell(trend)="row">
        <span class="trend-new" v-if="row.item.hits_previous === 0">
          Neu
        </span>
        <span v-else class="trend" :class="getTrendClass(row.item)"></span>
      </template>

      <template v-slot:cell(topReferrer)="row">
        <div class="top-referrers">
          <img class="top-referrer-logo" v-for="referrer in getTopReferrers(row.item)" :alt="referrer"
               :src="`${publicPath}vendor_logos/${referrer.toLowerCase()}.png`" :key="referrer"/>
        </div>
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
import Select from '@/components/Select.vue'
import { SelectReferrerMixin } from '@/common/SelectReferrerMixin'

interface Data {
  items: ArticleData[];
  rowItems: Array<any>;
  loadingState: LoadingState;
  defaultFields: any;
  publicPath: string;
}

interface Methods {
  loadData (timeframe: Timeframe): Promise<void>;
  toggleDetails (row: any): void;
  syncOpenedDetailsStateWithRoute (): void;
  formatSelectReferrer (value: null, key: string, item: ArticleData): string | undefined;
  getTrendClass (item: ArticleData): string;
  getTopReferrers (item: ArticleData): Array<string>;
}

interface Computed {
  availableReferrers: Array<string>;
  openedMsids: Array<number>;
  fields: any;
}

let currentRequestController: AbortController | null = null

export default Vue.extend<Data, Methods, Computed, {}>({
  name: 'BaseDashboardTable',
  components: {
    BTable,
    LoadingControl,
    ArticleRowDetail,
    Select
  },
  mixins: [SelectReferrerMixin],
  methods: {
    toggleDetails (item: any) {
      const query = this.$route.query.openMsids as string || '[]'
      let currentlyOpenMsids = JSON.parse(query)
      if (currentlyOpenMsids.includes(item.msid)) {
        currentlyOpenMsids = currentlyOpenMsids.filter((msid: number) => msid !== item.msid)
      } else {
        currentlyOpenMsids.push(item.msid)
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
      const referrer = item.referrers.find(({ referrer }) => {
        // @ts-ignore selectedReferrer is defined on mixin type inferrence fails
        return this.selectedReferrer === referrer
      })
      if (referrer) {
        return (`${referrer.hits.toString()} (${referrer.percentage.toLocaleString([], { style: 'percent' })})`)
      } else {
        return ''
      }
    },
    getTrendClass (item: ArticleData) {
      if (item.hits_previous === 0) {
        return ''
      } else {
        const trend = getTrend(item.hits_previous, item.hits, true)
        const arrowType = trend.direction * trend.score
        return `tazboard-trend-${arrowType}`
      }
    },
    getTopReferrers (item: ArticleData): Array<string> {
      return item.referrers
        .filter(({ percentage }) => percentage > TOP_REFERRER_THRESHOLD)
        .map(({ referrer }) => referrer)
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
    },
    fields () {
      if ([TimeframeId.KEY_15_MINUTES, TimeframeId.KEY_30_MINUTES, TimeframeId.KEY_1_HOURS].includes(this.$route.query.timeframeId as TimeframeId)) {
        const trendsColumnDefinition = {
          key: 'trend',
          label: '',
          tdClass: 'text-center align-middle',
          thClass: 'tazboard-dashboard-table-th'
        }
        const fields = this.defaultFields.slice()
        fields.splice(2, 0, trendsColumnDefinition)
        return fields
      } else {
        return this.defaultFields
      }
    }
  },
  data () {
    return {
      publicPath: process.env.BASE_URL,
      sortBy: null,
      sortDesc: false,
      rowItems: [],
      loadingStateTimeframe: LoadingState.FRESH,
      defaultFields: [
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
          sortable: true,
          formatter: (value: number) => value.toLocaleString()
        },
        {
          key: 'headline',
          label: 'Titel',
          tdClass: 'text-left',
          thClass: 'tazboard-dashboard-table-th tazboard-dashboard-table-th-title text-left'
        },
        {
          key: 'pubdate',
          label: 'veröffentlicht',
          tdClass: 'align-middle tazboard-dashboard-table-td-pubdate text-right',
          thClass: 'tazboard-dashboard-table-th text-center',
          formatter: formatPublicationTime,
          sortable: true
        }, {
          key: 'referrerSelect',
          label: 'Klicks über',
          tdClass: 'tazboard-dashboard-table-td-referrer-select align-middle text-right',
          thClass: 'tazboard-dashboard-table-th tazboard-dashboard-table-th-referrer-select tazboard-dashboard-table-th-black text-center',
          sortable: true,
          sortByFormatted: true,
          formatter: (value: null, key: string, item: ArticleData) => {
            // @ts-ignore type inference of this doesn't work here
            return this.formatSelectReferrer(value, key, item)
          }
        }, {
          key: 'topReferrer',
          label: 'Top Referrer',
          tdClass: 'text-right align-middle',
          thClass: 'tazboard-dashboard-table-th text-center'
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
<style lang="scss" scoped>
@import "src/style/variables";

.archive {
  background-color: $taz-archive;
}

.frontpage {
  background-color: $taz-highlight;
}

.trend {
  font-size: 1.5rem;
  line-height: 2;
  position: relative;
  top: 3px;
}

.trend-new {
  color: green;
  font-weight: bold;
}

.top-referrer-logo {
  width: 24px;
  margin: 0 2px;
}

</style>
