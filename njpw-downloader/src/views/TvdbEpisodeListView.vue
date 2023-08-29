<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { errorCallback } from '../common'
import TvdbEpisodeService from '../services/TvdbEpisodeService'

const route = useRoute()
const router = useRouter()
const episodes = ref([])

const fetchEpisodes = (serviceMethod, routeName) =>
  serviceMethod()
    .then((response) => {
      episodes.value = response.data
      router.push({ name: routeName })
    })
    .catch(errorCallback)

function getEpisodes() {
  fetchEpisodes(TvdbEpisodeService.getAll, 'viewTvdbEpisodes')
}

function getUnassociated() {
  fetchEpisodes(TvdbEpisodeService.getUnassociated, 'viewTvdbEpisodesUnassociated')
}

function getRecent() {
  fetchEpisodes(TvdbEpisodeService.getRecent, 'viewTvdbEpisodesRecent')
}

function deleteEpisode(id) {
  TvdbEpisodeService.delete(id)
    .then(() => {
      episodes.value = episodes.value.filter((e) => e.id !== id)
    })
    .catch(errorCallback)
}

function edit(id) {
  router.push({ name: 'viewTvdbEpisode', params: { id } })
}

let method = ''
if (route.name == 'viewTvdbEpisodes') {
  method = TvdbEpisodeService.getAll
} else if (route.name == 'viewTvdbEpisodesUnassociated') {
  method = TvdbEpisodeService.getUnassociated
} else if (route.name == 'viewTvdbEpisodesRecent') {
  method = TvdbEpisodeService.getRecent
}
fetchEpisodes(method, route.name)
</script>

<template>
  <div class="thead">
    <h1>TVDB Episodes</h1>
    <div class="filters">
      <button class="btn btn-light mx-1" @click="getEpisodes()">All episodes</button>
      <button class="btn btn-light mx-1" @click="getUnassociated()">Unassociated episodes</button>
      <button class="btn btn-light mx-1" @click="getRecent()">Recent downloads</button>
    </div>
  </div>
  <div class="container m-2 w-50">
    <div class="header row">
      <div class="col-sm-8">Title</div>
      <div class="col">Air Date</div>
      <div class="col-auto"></div>
    </div>
    <div class="tvdb-episode row" v-for="ep in episodes" :key="ep.id" :id="`tvdb-${ep.id}`">
      <div class="col-sm-8">{{ ep.title }}</div>
      <div class="col">{{ ep.air_date }}</div>
      <div class="btn-group my-1 col-auto">
        <button class="btn btn-primary" @click="edit(ep.id)">Edit</button>
        <button class="btn btn-danger" @click="deleteEpisode(ep.id)">X</button>
      </div>
    </div>
  </div>
</template>
