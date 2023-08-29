import { createRouter, createWebHistory } from 'vue-router'
import AssociationListView from '../views/AssociationListView.vue'
import AssociationView from '../views/AssociationView.vue'
import NjpwWorldEpisodeListView from '../views/NjpwWorldEpisodeListView.vue'
import NjpwWorldEpisodeView from '../views/NjpwWorldEpisodeView.vue'
import TvdbEpisodeListView from '../views/TvdbEpisodeListView.vue'
import TvdbEpisodeView from '../views/TvdbEpisodeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/associations'
    },
    {
      path: '/associations',
      name: 'associationList',
      component: AssociationListView
    },
    {
      path: '/associations/recent',
      name: 'associationListRecent',
      component: AssociationListView
    },
    {
      path: '/associations/create',
      name: 'newAssociation',
      component: AssociationView
    },
    {
      path: '/associations/:id',
      name: 'viewAssociation',
      component: AssociationView
    },
    {
      path: '/njpwEpisodes',
      name: 'viewNjpwEpisodes',
      component: NjpwWorldEpisodeListView
    },
    {
      path: '/njpwEpisodes/unassociated',
      name: 'viewNjpwEpisodesUnassociated',
      component: NjpwWorldEpisodeListView
    },
    {
      path: '/njpwEpisodes/recent',
      name: 'viewNjpwEpisodesRecent',
      component: NjpwWorldEpisodeListView
    },
    {
      path: '/njpwEpisodes/:id',
      name: 'viewNjpwEpisode',
      component: NjpwWorldEpisodeView
    },
    {
      path: '/tvdbEpisodes',
      name: 'viewTvdbEpisodes',
      component: TvdbEpisodeListView
    },
    {
      path: '/tvdbEpisodes/unassociated',
      name: 'viewTvdbEpisodesUnassociated',
      component: TvdbEpisodeListView
    },
    {
      path: '/tvdbEpisodes/recent',
      name: 'viewTvdbEpisodesRecent',
      component: TvdbEpisodeListView
    },
    {
      path: '/tvdbEpisodes/:id',
      name: 'viewTvdbEpisode',
      component: TvdbEpisodeView
    }
  ]
})

export default router
