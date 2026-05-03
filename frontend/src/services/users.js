import { api } from './api'

export const usersService = {
  getUsers() {
    return api('/users', { method: 'GET' })
  },
  createUser(data) {
    return api('/users/register', { method: 'POST', body: data })
  }
}
