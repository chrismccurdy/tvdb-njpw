<script setup>
import { reactive, ref } from 'vue'

defineProps(['title', 'confirmButtonText', 'closeButtonText'])

const visible = ref(false)
const actions = reactive({
  show: () => {
    visible.value = true
  },
  save: () => {
    console.log('doing nothing by default... override this method')
  },
  close: () => {
    visible.value = false
  }
})

defineExpose({ actions })
</script>

<template>
  <div class="modal-mask" v-if="visible">
    <div class="modal show">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button type="button" class="close" @click="actions.close()" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <slot name="modal-body">Default modal body text</slot>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary m-1" @click="actions.save()">
              {{ confirmButtonText }}
            </button>
            <button type="button" class="btn btn-secondary m-1" @click="actions.close()">
              {{ closeButtonText }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}

.modal.show {
  display: block;
}
</style>
