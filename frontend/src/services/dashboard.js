import { api } from './api'

export const dashboardService = {
  getSummary() {
    return api('/dashboard/summary', { method: 'GET' })
  }
}
