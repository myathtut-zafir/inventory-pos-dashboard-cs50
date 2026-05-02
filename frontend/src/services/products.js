import { api } from './api'

export const productsService = {
  getProducts() {
    return api('/products', { method: 'GET' })
  }
}
