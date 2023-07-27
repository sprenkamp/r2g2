<!-- <template>
    <h3>This is home page</h3>
    <el-button color="FFFFFF" type="primary" class="button1">
      <router-link to="/newspage" class="news">news</router-link>
    </el-button>

    <div>
      <h1>{{ $t('Select a country of interest') }}</h1>
      <p>{{ $t("all countries analysed") }}</p>
      <button @click="changeLocale('English')">English</button>
      <button @click="changeLocale('Deutsch')">Deutsch</button>
    </div>
</template>

<script>
export default {
  methods: {
    changeLocale(locale) {
      this.$i18n.locale = locale;
    }
  }
};

</script>

<style>

</style> -->

<template>
  <el-container class="layout-container" style="height: 700px">
    <el-aside width="400px">
      <el-scrollbar>
        <div class="m-4">
          <p>Sprache/Language</p>
          <el-select v-model="value" class="m-2" placeholder="Select Language" size="large">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
        <div class="m-4">
          <p>Choose the topics of interest within the telegram data</p>
          <el-select
            v-model="value1"
            multiple
            placeholder="Select"
            size="large"
          >
            <el-option
              v-for="item in options1"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
        <div class="m-4">
          <p>Choose the topics of interest within the news data</p>
          <el-select
            v-model="value2"
            multiple
            placeholder="Select"
            size="large"
          >
            <el-option
              v-for="item in options2"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>

      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
      </el-header>
      <el-main>
        <MapComponent />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import MapComponent from './MapComponent.vue';


export default {
  components: {
    MapComponent,
  },
  data() {
    return {
      value: '',
      value1: [],
      value2: [],
      options: [  
        {value: 'English', label: 'English'},
        {value: 'Deutsch', label: 'Deutsch'},
      ],
      options1: [
        // Define options for the first el-select here
      ],
      options2: [
        // Define options for the second el-select here
      ]
    };
  }
};
</script>


<style scoped>
.layout-container .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}
.layout-container .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}
.layout-container .el-main {
  padding: 0;
}

/* New styles for the map component */
.layout-container .el-main .map-component {
  width: 100%;
  height: 100%;
}

</style>
