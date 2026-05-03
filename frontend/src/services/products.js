import { api } from './api'

export const productsService = {
  getProducts() {
    return api('/products', { method: 'GET' })
  },
  createProduct(data) {
    return api('/products', { method: 'POST', body: data })
  },
  updateProduct(id, data) {
    return api(`/products/${id}`, { method: 'PATCH', body: data })
  },
  deleteProduct(id) {
    return api(`/products/${id}`, { method: 'DELETE' })
  }
}
