<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { errorCallback } from '../common'
import AssociationService from '../services/AssociationService'

const route = useRoute()
const router = useRouter()
const associations = ref(null)

const fetchAssociations = (serviceMethod, routeName) =>
  serviceMethod()
    .then((response) => {
      associations.value = response.data
      router.push({ name: routeName })
    })
    .catch(errorCallback)

function getAssociations() {
  fetchAssociations(AssociationService.getAll, 'associationList')
}

function getRecentAssociations() {
  fetchAssociations(AssociationService.getRecent, 'associationListRecent')
}

function deleteAssociation(id) {
  AssociationService.delete(id)
    .then((response) => {
      associations.value = associations.value.filter((a) => a.id !== id)
      console.log(response)
    })
    .catch(errorCallback)
}

function newAssociation() {
  router.push({ name: 'newAssociation' })
}

function edit(id) {
  router.push({ name: 'viewAssociation', params: { id } })
}

const method =
  route.name == 'associationListRecent' ? AssociationService.getRecent : AssociationService.getAll
fetchAssociations(method, route.name)
</script>

<template>
  <div class="thead">
    <h1>Associations</h1>
    <div class="filters">
      <button class="btn btn-light mx-1" @click="getAssociations()">All associations</button>
      <button class="btn btn-light mx-1" @click="getRecentAssociations()">
        Recent associations
      </button>
      <button class="btn btn-success mx-1" @click="newAssociation()">New association</button>
    </div>
  </div>
  <div class="container m-2">
    <div class="header row">
      <div class="col">TVDB Episode</div>
      <div class="col">NJPW World Episode</div>
      <div class="col-auto"></div>
    </div>
    <div
      class="association row"
      v-for="{ id, tvdb_episode, njpw_world_episode } in associations"
      v-bind:key="id"
      :id="`assoc-${id}`"
    >
      <div :id="`tvdb-${tvdb_episode.id}`" class="col">
        {{ tvdb_episode.title }} - {{ tvdb_episode.air_date }}
      </div>
      <div :id="`njpw-world-${njpw_world_episode.id}`" class="col">
        {{ njpw_world_episode.title }} - {{ njpw_world_episode.air_date }}
      </div>
      <div class="btn-group my-1 col-auto">
        <button class="btn btn-primary" @click="edit(id)">Edit</button>
        <button class="btn btn-danger" @click="deleteAssociation(id)">X</button>
      </div>
    </div>
  </div>
</template>
