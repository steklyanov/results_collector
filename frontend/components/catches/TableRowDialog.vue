<template>
  <v-dialog
    @click:outside="closeModal"
    v-model="dialog"
    max-width="800"
  >
    <template v-slot:activator="{ on, attrs }"/>

    <v-card v-if="row">
      <v-card-title >
        {{ Object.values(row)[0][0].name }}
      </v-card-title>

      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="Object.values(row)[0]"
          :items-per-page="5"
          class="elevation-1"
        >
          <template v-slot:item="{ item, index }">
            <tr>
              <td>
                {{item.name }}
              </td>
              <td>
                {{ item.datetime }}
              </td>
              <td>
                {{ item.external_id }}
              </td>
              <td>
                <img :src=" 'http://localhost:8000/media/' + item.img_path" aspect-ratio="1" width="100"></img>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          text
          @click="closeModal"
        >
          Закрыть окно
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
name: "TableRowDialog",
  props: ['dialog', 'row'],
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
  closeModal() {
    this.$emit('closeModal')

  }
  }
}
</script>

<style scoped>

</style>
