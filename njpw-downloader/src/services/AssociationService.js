import http from '../http-common'

class AssociationService {
  getAll() {
    return http.get('/api/associations/')
  }

  getRecent() {
    return http.get('/api/associations/recent/')
  }

  get(id) {
    return http.get(`/api/associations/${id}/`)
  }

  create(data) {
    return http.post('/api/associations/', data)
  }

  update(id, data) {
    return http.put(`/api/associations/${id}/`, data)
  }

  delete(id) {
    return http.delete(`/api/associations/${id}/`)
  }

  deleteAll() {
    return http.delete('/api/associations/')
  }
}

export default new AssociationService()
