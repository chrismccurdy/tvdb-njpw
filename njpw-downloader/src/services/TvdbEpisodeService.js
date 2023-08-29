import http from '../http-common'

class TvdbEpisodeService {
  getAll() {
    return http.get('/api/tvdb_episodes/')
  }

  getRecent() {
    return http.get('/api/tvdb_episodes/downloads/recent/')
  }

  getUnassociated() {
    return http.get('/api/tvdb_episodes/unassociated/')
  }

  get(id) {
    return http.get(`/api/tvdb_episodes/${id}/`)
  }

  create(data) {
    return http.post('/api/tvdb_episodes/', data)
  }

  update(id, data) {
    return http.put(`/api/tvdb_episodes/${id}/`, data)
  }

  delete(id) {
    return http.delete(`/api/tvdb_episodes/${id}/`)
  }

  deleteAll() {
    return http.delete('/api/tvdb_episodes/')
  }
}

export default new TvdbEpisodeService()
