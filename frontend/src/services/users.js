import { api } from './api'

export const usersService = {
  getUsers() {
    return api('/users', { method: 'GET' })
  }
}
