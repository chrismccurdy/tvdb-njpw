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

  getDownloads() {
    return http.get('/api/associations/download/status/')
  }

  downloadPending() {
    return http.post('/api/associations/download/')
  }

  download(id) {
    return http.post(`/api/associations/download/${id}/`)
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
