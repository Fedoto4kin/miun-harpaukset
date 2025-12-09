import axios from '@/axios'

const API_URL = '/v0/grammar/'

export const grammarService = {
  getAll(params = {}) {
    return axios.get(API_URL, { params })
  },
  
  getById(id) {
    return axios.get(`${API_URL}${id}/`)
  },
  
}

export default grammarService