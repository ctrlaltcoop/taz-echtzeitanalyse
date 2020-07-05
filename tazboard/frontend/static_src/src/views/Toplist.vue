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

const apiClient = new ApiClient()

interface ToplistData {
  items: ArticleData[];
}

interface ToplistMethods {
  update (minDate: string): void;
}

export default Vue.extend<ToplistData, ToplistMethods, {}>({
  name: 'Toplist',
  components: {
    BTable
  },
  methods: {
    async update (minDate: string) {
      this.items = ((await apiClient.toplist(minDate, 'now', 25)).data)
    }
  },
  data: () => {
    return {
      fields: [
        {
          key: 'value',
          label: 'Klicks',
          class: 'text-right',
          thClass: 'white-caption',
          formatter: (value) => value.toLocaleString(),
          sortable: true
        },
        {
          key: 'name',
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
        if (query.minDate) {
          this.update(query.minDate as string)
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
