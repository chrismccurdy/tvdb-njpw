import http from '../http-common'

class NjpwWorldSeriesService {
  getAll() {
    return http.get('/api/njpw_world_series/')
  }

  get(id) {
    return http.get(`/api/njpw_world_series/${id}/`)
  }

  create(data) {
    return http.post('/api/njpw_world_series/', data)
  }

  update(id, data) {
    return http.put(`/api/njpw_world_series/${id}/`, data)
  }

  delete(id) {
    return http.delete(`/api/njpw_world_series/${id}/`)
  }

  deleteAll() {
    return http.delete('/api/njpw_world_series/')
  }
}

export default new NjpwWorldSeriesService()
