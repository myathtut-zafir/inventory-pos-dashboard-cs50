import { ofetch } from 'ofetch'

export const api = ofetch.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  async onResponseError({ request, response, options }) {
    console.error(`[API Error] ${request}: ${response.status} ${response.statusText}`)
  }
})
