<template> 
  <Navigation/>
  <DatePicker v-if="minDate !== null && maxDate !== null" :minDate="minDate" :maxDate="maxDate" @selected-date="handleSelectedDate"/>
</template>
<script>
import Navigation from './Navigation.vue';
import DatePicker from './DatePicker.vue';

export default {
  components: {
    Navigation,
    DatePicker
  },
  data() {
    return{
      minDate: null,           // define min date
      maxDate: null,           // define max date
      dateOptions: [],         // define date options in time slider
    }
  },
  async created(){
    const newsPath = 'https://raw.githubusercontent.com/sprenkamp/r2g2/main/frontend/r2g2_vue/src/data/df_news_demo.csv'

    // get the min,max date as well as date range in type 1645660800000
    const dateData = await this.$getDate(newsPath);
    this.dateOptions = dateData;
    this.minDate = this.dateOptions[0];
    this.maxDate = this.dateOptions[this.dateOptions.length - 1];
    this.selectedDate = [this.minDate, this.maxDate];
  },
  methods: {
    async handleSelectedDate(value) {
      this.dateOptions = await this.$convertTimetoString(value);
      console.log(this.dateOptions)
    }
  }

}
</script>