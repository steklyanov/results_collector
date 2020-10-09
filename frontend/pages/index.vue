<template>
  <v-container>
    <catches-table/>
  </v-container>
</template>

<script>
import CatchesTable from "~/components/catches/CatchesTable";
import ZoneSelector from "@/components/polygon/ZoneSelector";

export default {
  components: {
    ZoneSelector,
    CatchesTable,
  }
}
</script>
