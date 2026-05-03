import { api } from './api'

export const salesService = {
  createSale(data) {
    return api('/sales', { method: 'POST', body: data })
  }
}
