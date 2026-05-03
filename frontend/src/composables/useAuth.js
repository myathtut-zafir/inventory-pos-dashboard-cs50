import { ref, computed } from 'vue'
import { api } from '../services/api'
import router from '../router'

const token = ref(localStorage.getItem('access_token'))

export const useAuth = () => {
  const login = async (username, password) => {
    // Using URLSearchParams which is typical for OAuth2 /auth/login endpoints
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    try {
      const res = await api('/auth/login', { 
        method: 'POST', 
        body: formData
      })
      
      if (res && res.access_token) {
        setToken(res.access_token)
        return { success: true }
      }
      return { success: false, error: 'Invalid response from server' }
    } catch (error) {
      return { 
        success: false, 
        error: error.data?.detail || 'Invalid username or password' 
      }
    }
  }

  const setToken = (newToken) => {
    localStorage.setItem('access_token', newToken)
    token.value = newToken
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    token.value = null
    router.push('/login')
  }

  const isAuthenticated = computed(() => !!token.value)

  const getUserRole = computed(() => {
    if (!token.value) return null
    try {
      const base64Url = token.value.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
      }).join(''))

      return JSON.parse(jsonPayload).role
    } catch (e) {
      console.error("Failed to decode token", e)
      return null
    }
  })

  return {
    token,
    login,
    logout,
    isAuthenticated,
    getUserRole
  }
}
