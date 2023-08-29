import http from '../http-common'

class TvdbSeriesService {
  getAll() {
    return http.get('/api/tvdb_series/')
  }

  get(id) {
    return http.get(`/api/tvdb_series/${id}/`)
  }

  create(data) {
    return http.post('/api/tvdb_series/', data)
  }

  update(id, data) {
    return http.put(`/api/tvdb_series/${id}/`, data)
  }

  delete(id) {
    return http.delete(`/api/tvdb_series/${id}/`)
  }

  deleteAll() {
    return http.delete('/api/tvdb_series/')
  }
}

export default new TvdbSeriesService()
