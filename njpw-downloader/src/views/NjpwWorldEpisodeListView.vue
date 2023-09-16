<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import EpisodeFilterModalWindow from '../components/EpisodeFilterModalWindow.vue'
import FilterDisplay from '../components/FilterDisplay.vue'

import { errorCallback, filtered } from '../common'
import NjpwWorldEpisodeService from '../services/NjpwWorldEpisodeService'

const route = useRoute()
const router = useRouter()
const episodes = ref([])
const modal = ref(null)
const filters = ref({})

const fetchEpisodes = (serviceMethod, routeName) =>
  serviceMethod()
    .then((response) => {
      episodes.value = response.data
      router.push({ name: routeName })
    })
    .catch(errorCallback)

function getEpisodes() {
  fetchEpisodes(NjpwWorldEpisodeService.getAll, 'viewNjpwEpisodes')
}

function getUnassociated() {
  fetchEpisodes(NjpwWorldEpisodeService.getUnassociated, 'viewNjpwEpisodesUnassociated')
}

function getRecent() {
  fetchEpisodes(NjpwWorldEpisodeService.getRecent, 'viewNjpwEpisodesRecent')
}

function formatDate(date) {
  return date == null ? '' : date.replace(/(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}).*/, '$1 $2')
}

function deleteEpisode(id) {
  NjpwWorldEpisodeService.delete(id)
    .then(() => {
      episodes.value = episodes.value.filter((e) => e.id !== id)
    })
    .catch(errorCallback)
}

function edit(id) {
  router.push({ name: 'viewNjpwEpisode', params: { id } })
}

let method = ''
if (route.name == 'viewNjpwEpisodes') {
  method = NjpwWorldEpisodeService.getAll
} else if (route.name == 'viewNjpwEpisodesUnassociated') {
  method = NjpwWorldEpisodeService.getUnassociated
} else if (route.name == 'viewNjpwEpisodesRecent') {
  method = NjpwWorldEpisodeService.getRecent
}

fetchEpisodes(method, route.name)
</script>

<template>
  <div class="thead">
    <h1>NJPW World Episodes</h1>
    <div class="filters">
      <button class="btn btn-light mx-1" @click="getEpisodes()">All episodes</button>
      <button class="btn btn-light mx-1" @click="getUnassociated()">Unassociated episodes</button>
      <button class="btn btn-light mx-1" @click="getRecent()">Recent downloads</button>
    </div>
  </div>
  <div class="container m-2">
    <div class="row align-items-center my-1">
      <div class="col-sm-1">
        <button @click="modal.showEpisodeFilterModal()" class="btn btn-primary m-1">Filters</button>
      </div>
      <div class="col">
        <FilterDisplay :filters="filters" />
      </div>
    </div>

    <div class="header row">
      <div class="col-sm-4">Title</div>
      <div class="col-sm-1">Air Date</div>
      <div class="col-sm">URL</div>
      <div class="col-sm-auto">Downloaded At</div>
      <div class="col-sm-1"></div>
    </div>
    <div
      class="njpw-episode row"
      v-for="ep in filtered(filters, episodes)"
      :key="ep.id"
      :id="`njpw-${ep.id}`"
    >
      <span class="col-sm-4">{{ ep.title }}</span>
      <span class="col-sm-1">{{ ep.air_date }}</span>
      <span class="col-sm">
        <a :href="ep.url">{{ ep.url }}</a>
      </span>
      <span class="col-sm-auto">{{ formatDate(ep.downloaded_at) }}</span>
      <div class="btn-group my-1 col-sm-1">
        <button class="btn btn-primary" @click="edit(ep.id)">Edit</button>
        <button class="btn btn-danger" @click="deleteEpisode(ep.id)">X</button>
      </div>
    </div>
  </div>

  <EpisodeFilterModalWindow ref="modal" @filters-updated="(f) => (filters = f)" />
</template>
