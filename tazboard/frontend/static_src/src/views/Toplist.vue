<template>
  <div class="row">
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

        <template v-slot:row-details="row">
          <ArticleRowDetail :article="row.item"/>
        </template>
      </BTable>
    </LoadingControl>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { getISOWeek, isToday, isYesterday } from 'date-fns'
import { BTable } from 'bootstrap-vue'

import { ApiClient } from '@/client/ApiClient'
import { ArticleData } from '@/dto/ToplistDto'
import { getTimeframeById, Timeframe } from '@/common/timeframe'
import { CAPTION_TODAY, CAPTION_YESTERDAY, TOP_REFERRER_THRESHOLD } from '@/common/constants'
import ArticleRowDetail from '@/components/ArticleRowDetail.vue'
import LoadingControl from '@/components/LoadingControl.vue'
import { LoadingState } from '@/common/LoadingState'

const apiClient = new ApiClient()

interface Data {
  items: ArticleData[];
  selectedReferrer: string | null;
  rowItems: Array<any>;
  loadingState: LoadingState;
}

interface Methods {
  update (timeframe: Timeframe): void;

  toggleDetails (row: any): void;

  syncOpenedDetailsStateWithRoute (): void;

  formatSelectReferrer (value: null, key: string, item: ArticleData): string | undefined;
}

interface Computed {
  availableReferrers: Array<string>;
  openedMsids: Array<number>;
}

let currentRequestController: AbortController | null = null

export default Vue.extend<Data, Methods, Computed, {}>({
  name: 'Toplist',
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
    async update (timeframe: Timeframe) {
      this.loadingState = LoadingState.LOADING
      try {
        if (currentRequestController !== null) {
          currentRequestController.abort()
        }
        currentRequestController = new AbortController()
        const { signal } = currentRequestController!!
        this.items = (await apiClient.toplist(timeframe.minDate, timeframe.maxDate, 25, {
          signal
        })).data
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
          label: 'Klicks',
          class: 'text-right',
          thClass: 'white-caption',
          formatter: (value: number) => value.toLocaleString(),
          sortable: true
        },
        {
          key: 'trend',
          label: '',
          class: 'text-center',
          formatter: (value: null, key: string, item: ArticleData) => {
            return (item.hits / item.hits_previous - 1).toLocaleString([], { style: 'percent' })
          }
        },
        {
          key: 'headline',
          label: 'Titel',
          class: 'text-left',
          thClass: 'white-caption',
          formatter: (value: null, key: string, item: ArticleData) => {
            return (item.hits / item.hits_previous - 1).toLocaleString([], { style: 'percent' })
          }
        },
        {
          key: 'pubdate',
          label: 'veröffentlicht',
          class: 'text-right',
          thClass: 'white-caption',
          formatter: (value: string | null) => {
            if (value === null) return
            const now = new Date()
            const pubDate = new Date(value)
            const thisWeek = getISOWeek(now)
            const pubWeek = getISOWeek(pubDate)
            if (isToday(pubDate)) {
              return CAPTION_TODAY
            } else if (isYesterday(pubDate)) {
              return CAPTION_YESTERDAY
            } else if (thisWeek === pubWeek) {
              return new Date(value).toLocaleDateString([], {
                weekday: 'long'
              })
            } else {
              return new Date(value).toLocaleDateString()
            }
          },
          sortable: true
        }, {
          key: 'referrerSelect',
          label: 'Klicks über',
          class: 'text-right',
          thClass: 'white-caption',
          formatter: (value: null, key: string, item: ArticleData) => {
            // @ts-ignore type inference of this doesn't work here
            return this.formatSelectReferrer(value, key, item)
          }
        }, {
          key: 'topReferrer',
          label: 'Top Referrer',
          class: 'text-right',
          thClass: 'white-caption',
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
          this.update(timeframe!!)
        }
        this.syncOpenedDetailsStateWithRoute()
      },
      immediate: true,
      deep: true
    }
  }
})
</script>

<!-- styles for vue table won't take effect unless unscoped -->
<style lang="scss">
@import 'src/style/variables';

.row-headline-headline {
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

.white-caption {
  color: $white;
  font-size: 2rem;
}
</style>

<style lang="scss" scoped>
.loading-control {
  min-height: 450px;
  flex-direction: column;
}

</style>
