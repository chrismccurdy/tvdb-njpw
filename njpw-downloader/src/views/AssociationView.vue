<script setup>
import { reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import AlertBox from '../components/AlertBox.vue'
import EpisodeSelectList from '../components/EpisodeSelectList.vue'
import EpisodeFilterModalWindow from '../components/EpisodeFilterModalWindow.vue'

import { useAlerts } from '../common'
import AssociationService from '../services/AssociationService'
import NjpwWorldEpisodeService from '../services/NjpwWorldEpisodeService'
import TvdbEpisodeService from '../services/TvdbEpisodeService'

const route = useRoute()
const router = useRouter()
const association = ref(null)
const tvdbEpisode = ref(null)
const njpwWorldEpisode = ref(null)
const tvdbEpisodes = ref([])
const njpwWorldEpisodes = ref([])
const unassociatedOnly = ref(true)
const { success, error } = useAlerts()
const successAlert = success.alert
const errorAlert = error.alert
const modal = ref(null)
const filters = reactive({})

function successCallback() {
  success.show('Association saved', 5)
}

function save() {
  error.hide()
  if (association.value == null) {
    association.value = {}
  }
  association.value.tvdb_episode = tvdbEpisode.value
  association.value.njpw_world_episode = njpwWorldEpisode.value
  if ('id' in association.value) {
    AssociationService.update(association.value.id, association.value)
      .then(successCallback)
      .catch(error.show)
  } else {
    AssociationService.create(association.value).then(successCallback).catch(error.show)
  }
}

function cancel() {
  router.go(-1)
}

function getEpisodes(unassociatedRef, episodesRef, service) {
  let fetchMethod = unassociatedRef.value ? service.getUnassociated : service.getAll
  return fetchMethod()
    .then((response) => {
      episodesRef.value = response.data
    })
    .catch(error.show)
}

function loadEpisodes() {
  getEpisodes(unassociatedOnly, tvdbEpisodes, TvdbEpisodeService)
  getEpisodes(unassociatedOnly, njpwWorldEpisodes, NjpwWorldEpisodeService)
}

async function loadAssociation() {
  if ('id' in route.params) {
    await AssociationService.get(route.params.id)
      .then((response) => {
        association.value = response.data
        tvdbEpisode.value = association.value.tvdb_episode.id
        njpwWorldEpisode.value = association.value.njpw_world_episode.id
        unassociatedOnly.value = false
        loadEpisodes()
      })
      .catch(error.show)
  } else {
    njpwWorldEpisode.value = { id: -1 }
    tvdbEpisode.value = { id: -1 }
    loadEpisodes()
  }
}

function updateFilters(f) {
  filters.series = f.series
  filters.year = f.year
  filters.month = f.month
}

function filtered(episodeList) {
  let filteredEpisodes = episodeList
  if (filters.series && filters.series.length > 0) {
    filteredEpisodes = filteredEpisodes.filter(
      (ep) => ep.series.title == filters.series || ep.series.name == filters.series
    )
  }
  if (filters.year && filters.year.length > 0) {
    filteredEpisodes = filteredEpisodes.filter((ep) => ep.air_date.startsWith(filters.year))
  }
  if (filters.month && filters.month.length > 0) {
    filteredEpisodes = filteredEpisodes.filter((ep) => ep.air_date.substring(5, 7) == filters.month)
  }
  return filteredEpisodes
}

loadAssociation()

watch(unassociatedOnly, loadEpisodes)
</script>

<template>
  <div class="thead">
    <h1>Association</h1>
  </div>
  <AlertBox ref="successAlert" alert-type="alert-success" />
  <AlertBox ref="errorAlert" alert-type="alert-danger" />

  <div class="container mx-0">
    <div class="row align-items-center my-1">
      <div class="col-sm-2"></div>
      <div class="col-sm-1">
        <button @click="modal.showEpisodeFilterModal()" class="btn btn-primary m-1">Filters</button>
      </div>
      <div class="col">
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
      </div>
    </div>

    <div class="row my-1">
      <div class="col-sm-2"></div>
      <div class="col-lg-8 form-check mx-3">
        <input
          class="form-check-input"
          id="unassociated"
          type="checkbox"
          v-model="unassociatedOnly"
        />
        <label class="form-check-label" for="unassociated">Unassociated Episodes Only</label>
      </div>
    </div>

    <div class="row my-1">
      <div class="label col-sm-2 my-2"><label for="tvdb-episode">TVDB Episode</label></div>
      <div class="input col-lg-8">
        <EpisodeSelectList v-model="tvdbEpisode" :episodes="filtered(tvdbEpisodes)" />
      </div>
    </div>

    <div class="row my-1">
      <div class="label col-sm-2 my-2"><label for="njpw-episode">NJPW World Episode</label></div>
      <div class="input col-lg-8">
        <EpisodeSelectList v-model="njpwWorldEpisode" :episodes="filtered(njpwWorldEpisodes)" />
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

  <EpisodeFilterModalWindow ref="modal" @filters-updated="(filters) => updateFilters(filters)" />
</template>
