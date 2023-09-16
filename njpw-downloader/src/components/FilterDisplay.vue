<script setup>
defineProps(['filters'])
</script>

<template>
  <span v-if="filters.series" class="m-2">
    <span class="label me-1">Series:</span>
    <span>{{ filters.series }}</span>
  </span>

  <span v-if="filters.year" class="m-2">
    <span class="label me-1">Year:</span>
    <span>{{ filters.year }}</span>
  </span>

  <span v-if="filters.month" class="m-2">
    <span class="label me-1">Month:</span>
    <span>{{ filters.month }}</span>
  </span>

  <span v-if="filters.hidden" class="m-2">
    <span class="label me-1">Hidden</span>
  </span>
</template>
