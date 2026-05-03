import { api } from './api'

export const productsService = {
  getProducts() {
    return api('/products', { method: 'GET' })
  },
  createProduct(data) {
    return api('/products', { method: 'POST', body: data })
  }
}
