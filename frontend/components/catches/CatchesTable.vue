<template>
  <v-container>

    <v-row>
      <v-col>
        <v-menu
        ref="date_from_emiter"
        v-model="date_from_emiter"
        :close-on-content-click="false"
        :return-value.sync="date_from"
        transition="scale-transition"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="date_from"
            label="События до"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="date_from"
          no-title
          scrollable
        >
          <v-spacer></v-spacer>
          <v-btn
            text
            color="primary"
            @click="date_from_emiter = false"
          >
            Cancel
          </v-btn>
          <v-btn
            text
            color="primary"
            @click="$refs.date_from_emiter.save(date_from)"
          >
            OK
          </v-btn>
        </v-date-picker>
      </v-menu>
      </v-col>
      <v-col>
        <v-menu
          ref="date_till_emiter"
          v-model="date_till_emiter"
          :close-on-content-click="false"
          :return-value.sync="date_till"
          transition="scale-transition"
          offset-y
          min-width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="date_till"
              label="События до"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="date_till"
            no-title
            scrollable
          >
            <v-spacer></v-spacer>
            <v-btn
              text
              color="primary"
              @click="date_till_emiter = false"
            >
              Cancel
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="$refs.date_till_emiter.save(date_till)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
      </v-col>
      <v-col>
        <v-btn @click="queryCatches">

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

export default {
name: "CatchesTable",
  components: {TableRowDialog},
  mounted() {
  this.$store.dispatch('getCatches', {"from": this.date_from, "till": this.date_till})
  },
  computed: {
    ...mapState([
      'catches'
    ])
  },
  data () {
    return {
      date_from_emiter: false,
      date_from: new Date().toISOString().substr(0, 10),

      date_till_emiter: false,
      date_till: new Date().toISOString().substr(0, 10),

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
    queryCatches() {
      this.$store.dispatch('getCatches', {"from": this.date_from, "till": this.date_till})
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
