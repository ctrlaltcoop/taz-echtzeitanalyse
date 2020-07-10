<template>
  <div class="row">
    <BTable class="w-100" :fields="fields" :items="items" thead-class="table-head">
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
    </BTable>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { BTable } from 'bootstrap-vue'
import { ApiClient } from '@/client/ApiClient'
import { ArticleData } from '@/dto/ToplistDto'
import { getTimeframeById, Timeframe } from '@/common/timeframe'
import { getISOWeek, isToday, isYesterday } from 'date-fns'
import { CAPTION_TODAY, CAPTION_YESTERDAY, TOP_REFERRER_THRESHOLD } from '@/common/constants'

const apiClient = new ApiClient()

interface Data {
  items: ArticleData[];
  selectedReferrer: string | null;
}

interface Methods {
  update (timeframe: Timeframe): void;
  formatSelectReferrer(value: null, key: string, item: ArticleData): string | undefined;
}

interface Computed {
  availableReferrers: Array<string>;
}

export default Vue.extend<Data, Methods, Computed>({
  name: 'Toplist',
  components: {
    BTable
  },
  methods: {
    async update (timeframe: Timeframe) {
      this.items = ((await apiClient.toplist(timeframe.minDate, timeframe.maxDate, 25)).data)
    },
    formatSelectReferrer (value: null, key: string, item: ArticleData): string | undefined {
      if (this.selectedReferrer === null) {
        this.selectedReferrer = item.referrers.data[0].referrertag
      }
      const selectedReferrer = this.selectedReferrer
      return item.referrers.data.find(({ referrertag }) => {
        return selectedReferrer === referrertag
      })?.percentage.toLocaleString([], { style: 'percent' })
    }
  },
  computed: {
    availableReferrers () {
      const allReferrers = this.items.map((item) => {
        return item.referrers.data.map((referrer) => referrer.referrertag)
      }).flat()
      return [...new Set(allReferrers)]
    }
  },
  data () {
    return {
      selectedReferrer: null,
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
          thClass: 'white-caption'
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
          // @ts-ignore type inference of this doesn't work here
          formatter: (value: null, key: string, item: ArticleData) => { return this.formatSelectReferrer(value, key, item) }
        }, {
          key: 'topReferrer',
          label: 'Top Referrer',
          class: 'text-right',
          thClass: 'white-caption',
          formatter: (value: null, key: string, item: ArticleData) => {
            return item.referrers.data
              .filter(({ percentage }) => percentage > TOP_REFERRER_THRESHOLD)
              .map(({ referrertag }) => referrertag)
              .join(',')
          }
        }
      ],
      items: []
    }
  },
  watch: {
    '$route.query': {
      handler (query: any) {
        if (query.timeframeId) {
          const timeframe = getTimeframeById(query.timeframeId)
          this.update(timeframe!!)
        }
      },
      immediate: true,
      deep: true
    }
  }
})
</script>
<style lang="scss">
@import 'src/style/variables';

.table-head {
  background-color: $taz-red;
}

.white-caption {
  color: $white;
  font-size: 2rem;
}

</style>
