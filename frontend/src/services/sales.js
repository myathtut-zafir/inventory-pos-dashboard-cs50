import { api } from './api'

export const salesService = {
  getSales() {
    return api('/sales', { method: 'GET' })
  },
  createSale(data) {
    return api('/sales', { method: 'POST', body: data })
  }
}
