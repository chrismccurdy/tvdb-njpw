<script setup>
import { computed } from 'vue'

const props = defineProps(['modelValue', 'episodes'])
const emit = defineEmits(['update:modelValue'])

const episode = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})
</script>

<template>
  <select v-model="episode" class="form-select">
    <option value="" disabled></option>
    <option v-for="ep in episodes" :key="ep.id" :value="ep.id">
      {{ ep.title }} - {{ ep.air_date }}
    </option>
  </select>
</template>
