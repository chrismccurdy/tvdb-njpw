<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAlerts } from '../common'
import AlertBox from '../components/AlertBox.vue'

import TvdbEpisodeService from '../services/TvdbEpisodeService'
import TvdbSeriesService from '../services/TvdbSeriesService'

const route = useRoute()
const router = useRouter()
const episode = ref(null)
const seriesList = ref([])
const { success, error } = useAlerts()
const successAlert = success.alert
const errorAlert = error.alert

async function getSeries() {
  await TvdbSeriesService.getAll()
    .then((response) => (seriesList.value = response.data))
    .catch(error.show)
}

function cancel() {
  router.go(-1)
}

function save() {
  error.hide()
  let ep = JSON.parse(JSON.stringify(episode.value))
  ep.series = episode.value.series.id
  if (ep.downloaded_at == '') {
    ep.downloaded_at = null
  }
  TvdbEpisodeService.update(ep.id, ep)
    .then(() => success.show('Episode saved', 5))
    .catch(error.show)
}

getSeries()
TvdbEpisodeService.get(route.params.id)
  .then((response) => (episode.value = response.data))
  .catch(error.show)
</script>

<template>
  <div class="thead">
    <h1>TVDB Episode</h1>
  </div>
  <AlertBox ref="successAlert" alert-type="alert-success" />
  <AlertBox ref="errorAlert" alert-type="alert-danger" />

  <div class="container mx-0" v-if="episode">
    <div class="row my-1">
      <div class="label col-sm-2 my-2"><label for="title">Title</label></div>
      <div class="input col-lg-8">
        <input
          id="title"
          name="title"
          class="form-control"
          v-model="episode.title"
          placeholder="Episode Title"
        />
      </div>
    </div>

    <div class="row my-1">
      <div class="label col-sm-2 my-2"><label for="air-date">Air Date</label></div>
      <div class="input col-lg-8">
        <input
          id="air-date"
          name="air-date"
          class="form-control w-25"
          v-model="episode.air_date"
          placeholder="Air Date"
        />
      </div>
    </div>

    <div class="row my-1">
      <div class="label col-sm-2 my-2"><label for="season">Season</label></div>
      <div class="input col-lg-8">
        <input
          id="season"
          name="season"
          class="form-control w-25"
          v-model="episode.season"
          placeholder="Season"
        />
      </div>
    </div>

    <div class="row my-1">
      <div class="label col-sm-2 my-2"><label for="episode">Episode</label></div>
      <div class="input col-lg-8">
        <input
          id="episode"
          name="episode"
          class="form-control w-25"
          v-model="episode.episode"
          placeholder="Episode"
        />
      </div>
    </div>

    <div class="row my-1">
      <div class="label col-sm-2 my-2"><label for="series">Series</label></div>
      <div class="input col-lg-8">
        <select class="form-select w-50" v-model="episode.series">
          <option value="" disabled></option>
          <option v-for="series in seriesList" :key="series.id" :value="series">
            {{ series.name }}
          </option>
        </select>
      </div>
    </div>

    <div class="row my-1">
      <div class="col-sm-2"></div>
      <div class="col-lg-8">
        <button class="btn btn-primary m-1" @click="save()">Save</button>
        <button class="btn btn-secondary m-1" @click="cancel()">Cancel</button>
      </div>
    </div>
  </div>
</template>
