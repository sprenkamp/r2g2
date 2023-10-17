<!-- MapComponent.vue -->

<!-- <template>
  <div>
    <div>
      <loading :active="isLoading" :is-full-page="true" :loader="loader" />
      <label for="checkbox">GeoJSON Visibility</label>
      <input
        id="checkbox"
        v-model="show"
        type="checkbox"
      >
      <label for="checkboxTooltip">Enable tooltip</label>
      <input
        id="checkboxTooltip"
        v-model="enableTooltip"
        type="checkbox"
      >
    </div>
    <l-map
      :zoom="mapOptions.zoom"
      :center="mapOptions.center"
      style="height: 500px; width: 100%"
      @ready="onMapReady"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      <l-geo-json
        v-if="show"
        :geojson="geojson"
        :options="options"
        :options-style="styleFunction"
      />
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LGeoJson } from "@vue-leaflet/vue-leaflet";
import { latLng } from "leaflet"; // important
import L from 'leaflet'

export default {
  name: "MapComponent",
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LMarker
  },
  props: {
    selectedCountry: String,
    selectedState: String,
  },
  data() {
    return {
      isLoading: false,
      fullPage: false,
      loader: "bars",
      show: true,
      enableTooltip: true,
      zoom: null,
      center: [50.449212, 7.734375],
      geojson: null,
      fillColor: "rgba(0, 0, 0, 0)",
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      mapOptions: {
        zoom: 6,
        center: [50.449212, 7.734375],
      },
    };
  },
  computed: {
    options() {
      return {
        onEachFeature: this.onEachFeatureFunction
      };
    },
    styleFunction() {
      const fillColor = this.fillColor; // important! need touch fillColor in computed for re-calculate when change fillColor
      return () => {
        return {
          weight: 2,
          color: "blue",
          opacity: 1,
          fillColor: fillColor,
          fillOpacity: 1
        };
      };
    },
    onEachFeatureFunction() {
      if (!this.enableTooltip) {
        return () => {};
      }
      return (feature, layer) => {
        layer.bindTooltip(
          "<div>Country:" +
            feature.properties.country +
            "</div><div>State: " +
            feature.properties.state +
            "</div>",
          { permanent: false, sticky: true }
        );
        layer.on({
          mouseover: this.highlightFeature,
          mouseout: this.resetHighlight,
          click: this.zoomToFeature,
        });
      };
    },
    language() {
      return {
        lanGermany: this.$t("Germany"),
        lanSwitzerland: this.$t("Switzerland"),
      }
    },

  },
  async created() {
    this.isLoading = true;
    const response = await fetch("https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/germany_switzerland.geojson")
    const data = await response.json();
    this.geojson = data;

    this.isLoading = false;
  },
  watch: {
    selectedCountry: "updateMapAndCenter",
  },
  methods: {
    async updateMapAndCenter() {
      this.updateMapZoom();
      const delay = 200;
      await new Promise(resolve => setTimeout(resolve, delay));
      this.updateMapCenter();
    },
    updateMapZoom(){
      if (this.selectedCountry === this.language.lanGermany) {
        this.mapOptions.zoom = 6;
      } else if (this.selectedCountry === this.language.lanSwitzerland) {
        this.mapOptions.zoom = 6;
      } else {
        this.mapOptions.zoom = 6;
      }
      console.log("Applied Zoom:", this.mapOptions.zoom);
    },
    updateMapCenter(){
      if (this.selectedCountry === this.language.lanGermany) {
        this.mapOptions.center = [51.0663, 10.4515];
      } else if (this.selectedCountry === this.language.lanSwitzerland) {
        this.mapOptions.center = [46.8182, 8.2275];
      } else {
        this.mapOptions.center = [50.449212, 7.734375];
      }
      console.log("Applied Center:", this.mapOptions.center);
    },
    onMapReady(map) {
      map.on("zoomend", () => {
        this.mapOptions.zoom = map.getZoom();
        console.log("Updated Zoom:", this.mapOptions.zoom);
      });
      map.on("moveend", () => {
        this.mapOptions.center = map.getCenter();
        console.log("Updated Center:", this.mapOptions.center);
      });
      this.mapInstance = map;
    },

    // 高亮 鼠标悬停
    highlightFeature(e) {
    const layer = e.target;
      layer.setStyle({
          weight: 5,
          color: 'yellow',
          dashArray: '',
          fillOpacity: 0.7
      });
      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }
    },
    // mouseout
    resetHighlight(e) {
    const layer = e.target;
      layer.setStyle({
        weight: 2,
        color: "blue",
        opacity: 1,
        fillColor: this.fillColor,
        fillOpacity: 1
      });
    },
    // zoom automatically
    zoomToFeature(e) {
      const selectedState = e.target.feature.properties.state;
      this.$emit('stateSelected', selectedState);
      this.mapInstance.fitBounds(e.target.getBounds());
    },
  },
};
</script> -->

<template>
  <div>
    <div>
      <loading :active="isLoading" :is-full-page="true" :loader="loader" />
      <label for="checkbox">GeoJSON Visibility</label>
      <input
        id="checkbox"
        v-model="show"
        type="checkbox"
      >
      <label for="checkboxTooltip">Enable tooltip</label>
      <input
        id="checkboxTooltip"
        v-model="enableTooltip"
        type="checkbox"
      >
    </div>
    <l-map
      :zoom="mapOptions.zoom"
      :center="mapOptions.center"
      style="height: 500px; width: 100%"
      @ready="onMapReady"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      <l-geo-json
        v-if="show"
        :geojson="geojson"
        :options="options"
        :options-style="styleFunction"
      />
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LGeoJson } from "@vue-leaflet/vue-leaflet";
import L from 'leaflet'

export default {
  name: "MapComponent",
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
  },
  data() {
    return {
      isLoading: false,
      loader: "bars",
      show: true,
      enableTooltip: true,
      zoom: null,
      center: [46.8182, 8.2275],
      geojson: null,
      fillColor: "rgba(0, 0, 0, 0)",
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      mapOptions: {
        zoom: 6.5,
        center: [46.8182, 8.2275], 
      },
    };
  },
  computed: {
    options() {
      return {
        onEachFeature: this.onEachFeatureFunction
      };
    },
    styleFunction() {
      const fillColor = this.fillColor; // important! need touch fillColor in computed for re-calculate when change fillColor
      return () => {
        return {
          weight: 2,
          color: "blue",
          opacity: 1,
          fillColor: fillColor,
          fillOpacity: 1
        };
      };
    },
    onEachFeatureFunction() {
      if (!this.enableTooltip) {
        return () => {};
      }
      return (feature, layer) => {
        layer.bindTooltip(
          "<div>Country:" +
            feature.properties.country +
            "</div><div>State: " +
            feature.properties.state +
            "</div>",
          { permanent: false, sticky: true }
        );
        layer.on({
          mouseover: this.highlightFeature,
          mouseout: this.resetHighlight,
          click: this.zoomToFeature,
        });
      };
    },
  },
  async created() {
    this.isLoading = true;
    const response = await fetch("https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/germany_switzerland.geojson")
    const data = await response.json();

    // only use swiss part
    const switzerlandFeatures = data.features.filter(feature => feature.properties.country === "Switzerland");
    this.geojson = {
      type: "FeatureCollection",
      features: switzerlandFeatures,
    };

    this.isLoading = false;
  },
  methods: {
    onMapReady(map) {
      map.on("zoomend", () => {
        this.mapOptions.zoom = map.getZoom();
      });
      map.on("moveend", () => {
        this.mapOptions.center = map.getCenter();
      });
      this.mapInstance = map;
    },

    // 高亮 鼠标悬停
    highlightFeature(e) {
      const layer = e.target;
      layer.setStyle({
          weight: 5,
          color: 'yellow',
          dashArray: '',
          fillOpacity: 0.7
      });
      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }
    },
    // mouseout
    resetHighlight(e) {
      const layer = e.target;
      layer.setStyle({
        weight: 2,
        color: "blue",
        opacity: 1,
        fillColor: this.fillColor,
        fillOpacity: 1
      });
    },
    // zoom automatically
    zoomToFeature(e) {
      const selectedState = e.target.feature.properties.state;
      this.$emit('stateSelected', selectedState);
      this.mapInstance.fitBounds(e.target.getBounds());
    },
  },
};
</script>
