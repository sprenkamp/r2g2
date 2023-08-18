<template>
  <div>
    <h3>This is Test Page</h3>
    <el-button color="FFFFFF" type="primary" class="button1">
      <router-link to="/" class="test">back</router-link>
    </el-button>
    <ul>
      <li v-for="item in data" :key="item._id">
        <p>ID: {{ item._id }}</p>
        <p>Name: {{ item.name }}</p>
        <p>Email: {{ item.email }}</p>
        <p>Date: {{ item.date }}</p>
        <hr>
      </li>
    </ul>
  </div>
</template>

<script>
import api from '../router/api.js'

export default {
  data() {
    return {
      data: []
    }
  },
  mounted() {
    this.fetch();
  },
  methods: {
    fetch() {
      api
        .getMongoTest()
        .then((response) => {
          this.data = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
}
</script>
