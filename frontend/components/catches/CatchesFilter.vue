<template>

  <v-row dense>
    <v-col cols="5" >
      <v-menu
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            v-model="dateFrom"
            label="С"
            dense
            prepend-icon="mdi-calendar"
            readonly
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker v-model="dateFrom"></v-date-picker>
      </v-menu>
    </v-col>
    <v-col cols="5">

      <v-menu
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            v-model="dateTo"
            label="По"
            dense
            prepend-icon="mdi-calendar"
            readonly
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker v-model="dateTo"></v-date-picker>
      </v-menu>
    </v-col>

    <v-col cols="2" align-self="center" align="end">
      <v-btn
        color="secondary"
        @click="applyFilter"
      >Применить
      </v-btn>
    </v-col>
  </v-row>
</template>


<script>
export default {
  data: () => ({
    dateTo: new Date().toISOString().substr(0, 10),
    dateFrom: new Date().toISOString().substr(0, 10)
  }),
  methods: {
    getTimestampFromDate(date, end) {
      if (end) {
        date.setHours(23, 59, 59)
      } else {
        date.setHours(0, 0, 0)
      }
      return Math.floor(date.getTime() / 1000)
    },
    applyFilter() {
      let dateTo = this.dateTo;
      if (dateTo == null) {
        dateTo = new Date().toISOString().substr(0, 10);
      }
      let timestampFrom = this.getTimestampFromDate(new Date(this.dateFrom), false);
      let timestampTo = this.getTimestampFromDate(new Date(dateTo), true);

      let filter = {
        dateTo: timestampTo,
        dateFrom: timestampFrom,
      }

      this.$emit('filter-apply', filter)
    }
  }
}
</script>

