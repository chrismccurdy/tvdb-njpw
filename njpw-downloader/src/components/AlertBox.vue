<script setup>
import { ref } from 'vue'

defineProps(['alertType'])

const message = ref('')
const div = ref(null)

const setMessage = (msg) => {
  message.value = msg
  div.value.classList.remove('collapse')
  div.value.classList.add('show')
}

const hideMessage = () => {
  div.value.classList.remove('show')
  div.value.classList.add('collapse')
}

defineExpose({ setMessage, hideMessage })
</script>

<template>
  <div class="alert fade collapse m-3" role="alert" ref="div" :class="alertType">
    <span ref="span">{{ message }}</span>
  </div>
</template>
