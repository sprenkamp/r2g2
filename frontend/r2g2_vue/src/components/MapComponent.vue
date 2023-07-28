<template>
  <l-map :zoom="13" :center="center">
    <l-tile-layer :url="url" :attribution="attribution" />
  </l-map>

</template>

<script>
import { LMap, LTileLayer } from "vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
  },
  data() {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '© OpenStreetMap contributors',
      center: [47.413220, -1.219482],
    }
  },
}
</script>

<style scoped>
.l-map {
  height: 500px;
  width: 100%;
}
</style>
