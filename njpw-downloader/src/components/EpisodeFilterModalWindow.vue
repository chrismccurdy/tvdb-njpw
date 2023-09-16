<script setup>
import { ref } from 'vue'
import ModalWindow from './ModalWindow.vue'

defineProps({
  series: {
    type: Boolean,
    default: true
  },
  year: {
    type: Boolean,
    default: true
  },
  month: {
    type: Boolean,
    default: true
  },
  hidden: {
    type: Boolean,
    default: true
  }
})
const emit = defineEmits(['filtersUpdated'])

const modal = ref(null)
const title = ref('Episode Filter')
const confirmButtonText = ref('Apply filters')
const closeButtonText = ref('Cancel')

const seriesFilter = ref(null)
const yearFilter = ref(null)
const monthFilter = ref(null)
const hiddenFilter = ref(false)

function showEpisodeFilterModal() {
  modal.value.actions.save = () => {
    modal.value.actions.close()
    emit('filtersUpdated', {
      series: seriesFilter.value,
      year: yearFilter.value,
      month: monthFilter.value,
      hidden: hiddenFilter.value
    })
  }
  modal.value.actions.show()
}

defineExpose({ showEpisodeFilterModal })
</script>

<template>
  <ModalWindow
    ref="modal"
    :title="title"
    :confirm-button-text="confirmButtonText"
    :close-button-text="closeButtonText"
  >
    <template v-slot:modal-body>
      <div class="container mx-0">
        <div class="row my-1" v-if="series">
          <div class="label col-sm-2 my-2"><label for="series-filter">Series</label></div>
          <div class="input col-lg-8">
            <select id="series-filter" name="series-filter" v-model="seriesFilter">
              <option></option>
              <option>New Japan Pro-Wrestling</option>
              <option>NJPW Strong</option>
            </select>
          </div>
        </div>

        <div class="row my-1" v-if="year">
          <div class="label col-sm-2 my-2"><label for="year-filter">Year</label></div>
          <div class="input col-lg-8">
            <input
              name="year-filter"
              id="year-filter"
              class="form-control w-25"
              v-model="yearFilter"
            />
          </div>
        </div>

        <div class="row my-1" v-if="month">
          <div class="label col-sm-2 my-2"><label for="month-filter">Month</label></div>
          <div class="input col-lg-8">
            <input
              name="month-filter"
              id="month-filter"
              class="form-control w-25"
              v-model="monthFilter"
            />
          </div>
        </div>

        <div class="row my-1" v-if="hidden">
          <div class="label col-sm-2 my-2"></div>
          <div class="input form-check mx-3 col-lg-8">
            <input class="form-check-input" id="hidden" type="checkbox" v-model="hiddenFilter" />
            <label class="form-check-label" for="hidden">Hidden</label>
          </div>
        </div>
      </div>
    </template>
  </ModalWindow>
</template>
