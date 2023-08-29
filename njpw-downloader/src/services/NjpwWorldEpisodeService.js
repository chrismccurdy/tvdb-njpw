import http from '../http-common'

class NjpwWorldEpisodeService {
  getAll() {
    return http.get('/api/njpw_world_episodes/')
  }

  getRecent(limit = 5) {
    return http.get(`/api/njpw_world_episodes/downloads/recent/${limit}/`)
  }

  getUnassociated() {
    return http.get('/api/njpw_world_episodes/unassociated/')
  }

  get(id) {
    return http.get(`/api/njpw_world_episodes/${id}/`)
  }

  create(data) {
    return http.post('/api/njpw_world_episodes/', data)
  }

  update(id, data) {
    return http.put(`/api/njpw_world_episodes/${id}/`, data)
  }

  delete(id) {
    return http.delete(`/api/njpw_world_episodes/${id}/`)
  }

  deleteAll() {
    return http.delete('/api/njpw_world_episodes/')
  }
}

export default new NjpwWorldEpisodeService()
