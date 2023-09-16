<script setup>
import { ref, watch } from 'vue'
import { errorCallback, useProgressToast } from '../common'
import AssociationService from '../services/AssociationService'

const downloads = ref([])
const task = ref(null)
const progressToast = useProgressToast()
const visible = progressToast.visible

function show() {
  progressToast.show()
}

function close() {
  progressToast.hide()
}

function toggle() {
  progressToast.visible.value = !progressToast.visible.value
}

function getDownloads() {
  AssociationService.getDownloads()
    .then((response) => {
      downloads.value = response.data
    })
    .catch(errorCallback)
}

function refreshDownloads() {
  if (progressToast.visible.value) {
    getDownloads()
    task.value = setInterval(getDownloads, 5000)
  } else {
    clearInterval(task.value)
    task.value = null
  }
}

defineExpose({ close, show, toggle })

watch(progressToast.visible, refreshDownloads)
</script>

<template>
  <div class="toast-container position-fixed bottom-0 end-0 p-3" v-if="visible">
    <div
      class="toast align-items-center show"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="toast-header">
        <strong class="me-auto">Downloads</strong>
        <button
          type="button"
          class="btn-close me-2 m-auto"
          @click="close()"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body">
        <span v-if="downloads.length == 0">No active downloads</span>
        <div v-else v-for="{ filename, progress } in downloads" v-bind:key="filename">
          <span>{{ filename }}</span>
          <div
            class="progress"
            role="progressbar"
            v-bind:aria-valuenow="progress"
            style="height: 5px"
          >
            <div class="progress-bar" v-bind:style="'width: ' + progress + '%'"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.toast.show {
  display: block;
}
</style>
