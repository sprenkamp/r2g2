<!-- DatePicker.vue -->

<template>
    <div class="demo-date-picker">
        <div class="block">
            <el-date-picker
                v-model="value"
                type="daterange"
                range-separator="To"
                start-placeholder="Start Date"
                end-placeholder="End Date"
                format="YYYY/MM/DD"
                value-format="YYYY-MM-DD"
                :disabled-date="disabledDate"
                :default-value="[minDate, maxDate]"
                @change="handleDateChange"
            >
            </el-date-picker>
        </div>
    </div>
</template>
  
<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const { minDate, maxDate } = defineProps(['minDate', 'maxDate'])
const emits = defineEmits()
const value = ref([minDate, maxDate])
const disabledDate = (time) => {
    if (minDate && maxDate) {
        return time < new Date(minDate) || time > new Date(maxDate)
    }
    return false
}

// transfer data
const handleDateChange = (value) => {
    emits('selected-date', value)
}
</script>

<style scoped>
</style>
  