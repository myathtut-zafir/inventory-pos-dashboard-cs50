import { api } from './api'

export const dashboardService = {
  getSummary() {
    return api('/dashboard/summary', { method: 'GET' })
  },
  getSalesByMonth() {
    return api('/dashboard/sales-by-month', { method: 'GET' })
  },
  getUsersByRole() {
    return api('/dashboard/users-by-role', { method: 'GET' })
  }
}
