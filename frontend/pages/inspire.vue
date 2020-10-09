<template>
  <v-container>
    <v-dialog  v-model="show_zone"  v-if="show_zone"  dark max-width="1000px" @click:outside="clickOutside">
      <zone-selector :v-if="show_zone"  :image_path="image_path" :polygon="polygon" :camera_id="camera_id" ></zone-selector>
    </v-dialog>
    <v-btn @click="editZone()">
      ПОЛИГОНЫ
    </v-btn>
  </v-container>
</template>

<script>
import ZoneSelector from "@/components/polygon/ZoneSelector";

export default {
  components: {
    ZoneSelector
  },
  mounted() {
    this.getScreenshot()
  },
  data () {
    return {
      show_zone: false,
      image_path: null,
      camera_id: null,
      polygon: null
    }
  },
  methods: {
    editZone(item) {
      console.log(item, "ITEM")
      this.getCamera()
      this.camera_id = 1

    },
    clickOutside() {
      console.log("clean outside")
      this.polygon = null
      this.camera_id = null
      this.show_zone = false
    },
    async getCamera() {
      this.$axios
        .get("api/v1/polygon/get_camera/" + `${1}/`)
        .then(r => {
          console.log(r)
          this.polygon = r.data.polygon
          this.show_zone = !this.show_zone
        })
    },
    async getScreenshot() {
      this.$axios
        .get("api/v1/collector/last_photo/")
        .then(r => {
          console.log(r)
          this.image_path = "http://localhost:8000" + r.data.image
        })
    }
  }
}

</script>
