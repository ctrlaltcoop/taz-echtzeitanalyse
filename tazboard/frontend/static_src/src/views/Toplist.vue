<template>
  <div class="row">
    <BTable class="w-100" :fields="fields" :items="items" thead-class="table-head" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { BTable } from 'bootstrap-vue'
import { ApiClient } from '@/client/ApiClient'
import { ArticleData } from '@/dto/ToplistDto'
import { getTimeframeById, Timeframe } from '@/common/timeframe'

const apiClient = new ApiClient()

interface ToplistData {
  items: ArticleData[];
}

interface ToplistMethods {
  update (timeframe: Timeframe): void;
}

export default Vue.extend<ToplistData, ToplistMethods, {}>({
  name: 'Toplist',
  components: {
    BTable
  },
  methods: {
    async update (timeframe: Timeframe) {
      this.items = ((await apiClient.toplist(timeframe.minDate, timeframe.maxDate, 25)).data)
    }
  },
  data: () => {
    return {
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
          key: 'headline',
          label: 'Titel',
          class: 'text-left',
          thClass: 'white-caption'
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
