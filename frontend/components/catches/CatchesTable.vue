<template>
  <v-container>

    <v-row>
      <v-col>
        <catches-filter @filter-apply="onFilterAccept" />
      </v-col>
      <v-col>
        <v-btn @click="downloadReport">
          Выгрузить отчет
        </v-btn>
      </v-col>
    </v-row>
    <table-row-dialog @closeModal="changeModalStatus" :dialog="dialog" :row="row" />
    <v-data-table
      v-if="catches"
      :headers="headers"
      :items="catches.catches"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:item="{ item, index }">
        <tr
          @click="onRowClick(item, index)">
          <td>
            {{ Object.values(item)[0][0].name }}
          </td>
          <td>
            {{ Object.values(item)[0][Object.values(item)[0].length - 1].datetime }}
          </td>
          <td>
            {{ Object.values(item)[0][0].external_id }}
          </td>
          <td>
            <img :src="Object.values(item)[0][0].img_path" aspect-ratio="1" width="100"></img>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>

</template>

<script>

import { mapState } from 'vuex';
import TableRowDialog from "@/components/catches/TableRowDialog";
import CatchesFilter from "@/components/catches/CatchesFilter";

export default {
name: "CatchesTable",
  components: {TableRowDialog, CatchesFilter},
  mounted() {
  this.$store.dispatch('getCatches', '')
  },
  computed: {
    ...mapState([
      'catches'
    ])
  },
  data () {
    return {
      date_from_emiter: false,
      date_from: null,

      date_till_emiter: false,
      date_till: null,

      dialog: false,
      row: null,
      headers: [
        {
          text: 'Имя',
          align: 'start',
          sortable: false,
          value: 'person.name',
        },
        {
          text: 'Дата',
          align: 'start',
          sortable: false,
          value: 'datetime',
        },
        {
          text: 'UUID',
          align: 'start',
          sortable: false,
          value: 'person.ex_id',
        },
        {
          text: 'Фото',
          align: 'start',
          sortable: false,
          value: 'image',
        },
      ]
    }
  },
  methods: {
    downloadReport() {
      this.$store.dispatch('getCatches', `?from=${this.date_from}&till=${this.date_till}&report=True`)

    },
    onFilterAccept(filter) {
      this.date_till = filter.dateTo;
      this.date_from = filter.dateFrom;
      this.queryCatches();
    },

    queryCatches() {
      this.$store.dispatch('getCatches', `?from=${this.date_from}&till=${this.date_till}`)
      console.log(this.date_from, this.date_till)

    },
  onRowClick(row, index) {
    this.row = row
    this.changeModalStatus()
    console.log(row)
  },
  changeModalStatus() {
    this.dialog = !this.dialog
  }
  }
}
</script>

<style scoped>

</style>
