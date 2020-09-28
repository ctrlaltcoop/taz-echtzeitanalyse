<template>
  <div class="row-detail mr-5 ml-5 pb-3 row">
    <div class="col-8 h-100 d-flex flex-column">
      <p class="tazboard-detail-caption">Top 5 Artikel im Schwerpunkt</p>
      <LoadingControl :loading-state="loadingState">
        <BTable
          small
          :items="toplist"
          :fields="toplistFields"
        />
      </LoadingControl>
    </div>
    <div class="referrers col-4">
      <p class="tazboard-detail-caption">Referrer</p>
      <GraphContainer
        class="tazboard-graph-container"
        :chart-component="referrerChartComponent"
        :graph-data="item.referrers"
      />
    </div>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'

import { ApiClient } from '@/client/ApiClient'
import { TimeframeMixin } from '@/common/timeframe'
import { SubjectsData } from '@/dto/SubjectsDto'
import { LoadingState } from '@/common/LoadingState'
import ReferrerBar from '@/components/graphs/charts/ReferrerBar.vue'
import { ArticleData } from '@/dto/ToplistDto'
import {
  CAPTION_TODAY,
  CAPTION_YESTERDAY,
  SUBJECT_DETAIL_TOPLIST_LIMIT
} from '@/common/constants'
import { BTable } from 'bootstrap-vue'
import GraphContainer from '@/components/graphs/GraphContainer.vue'
import LoadingControl from '@/components/LoadingControl.vue'
import { getISOWeek, isToday, isYesterday } from 'date-fns'
import { CONNECTION_ALERT_EVENT, ConnectionAlertBus } from '@/common/ConnectionAlertBus'

const apiClient = new ApiClient()

interface Props {
  item: SubjectsData;
}

interface Data {
  referrerChartComponent: typeof ReferrerBar;
  toplist: Array<ArticleData>;
  toplistFields: object;
  loadingState: LoadingState;
}

interface Methods {
  fetchToplist (): Promise<void>;
}

export default Vue.extend<Data, Methods, {}, Props>({
  name: 'SubjectRowDetail',
  props: {
    item: Object
  },
  components: {
    BTable,
    GraphContainer,
    LoadingControl
  },
  mixins: [TimeframeMixin],
  data () {
    return {
      referrerChartComponent: ReferrerBar,
      toplist: [],
      toplistFields: [
        {
          key: 'hits',
          label: 'Pageviews',
          class: 'text-right',
          formatter: (value: number) => value.toLocaleString()
        },
        {
          key: 'headline',
          label: 'Titel',
          class: 'text-left'
        },
        {
          key: 'pubdate',
          label: 'veröffentlicht',
          class: 'text-right',
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
          }
        }
      ],
      loadingState: LoadingState.FRESH
    }
  },
  methods: {
    async fetchToplist () {
      this.loadingState = this.loadingState !== LoadingState.SUCCESS ? LoadingState.LOADING : LoadingState.UPDATING
      try {
        this.toplist = (await apiClient.toplist(
          // @ts-ignore typescript won't infer types from vue mixins unfortunately
          this.currentTimeframe.minDate(),
          // @ts-ignore typescript won't infer types from vue mixins unfortunately
          this.currentTimeframe.maxDate(),
          SUBJECT_DETAIL_TOPLIST_LIMIT,
          this.item.subject_name
        )).data
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
    }
  },
  mounted () {
    this.fetchToplist()
  }
})
</script>
