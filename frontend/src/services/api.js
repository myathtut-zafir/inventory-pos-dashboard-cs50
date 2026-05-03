import { ofetch } from 'ofetch'
import router from '../router'

export const api = ofetch.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  onRequest({ request, options }) {
    const token = localStorage.getItem('access_token')
    if (token) {
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`
      }
    }
  },
  async onResponseError({ request, response, options }) {
    console.error(`[API Error] ${request}: ${response.status} ${response.statusText}`)
    if (response.status === 401) {
      localStorage.removeItem('access_token')
      // Push to login if not already there to avoid redirect loops
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login')
      }
    }
  }
})
