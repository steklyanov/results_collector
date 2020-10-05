<template>
  <v-container>
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
            <img :src=" 'http://localhost:8000/media/' + Object.values(item)[0][0].img_path" aspect-ratio="1" width="100"></img>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>

</template>

<script>

import { mapState } from 'vuex';
import TableRowDialog from "@/components/catches/TableRowDialog";

export default {
name: "CatchesTable",
  components: {TableRowDialog},
  mounted() {
  this.$store.dispatch('getCatches')
  },
  computed: {
    ...mapState([
      'catches'
    ])
  },
  data () {
    return {
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
  onRowClick(row, index) {
    this.row = row
    this.changeModalStatus()
    console.log(row)
  },
  changeModalStatus() {
    console.log("forrrrrrrrm")
    this.dialog = !this.dialog
  }
  }
}
</script>

<style scoped>

</style>
