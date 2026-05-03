<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { useToast } from 'primevue/usetoast'

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const router = useRouter()
const auth = useAuth()
const toast = useToast()

const handleLogin = async () => {
  isLoading.value = true
  const result = await auth.login(username.value, password.value)
  isLoading.value = false
  
  if (result.success) {
    toast.add({ severity: 'success', summary: 'Welcome', detail: 'Logged in successfully', life: 3000 })
    router.push('/')
  } else {
    toast.add({ severity: 'error', summary: 'Login Failed', detail: result.error, life: 5000 })
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <i class="pi pi-box logo"></i>
        <h1>Inventory POS</h1>
        <p>Sign in to access your dashboard</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <div class="input-wrapper">
            <i class="pi pi-user input-icon"></i>
            <input 
              id="username" 
              type="text" 
              v-model="username" 
              placeholder="Enter your username"
              required
            >
          </div>
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-wrapper">
            <i class="pi pi-lock input-icon"></i>
            <input 
              id="password" 
              type="password" 
              v-model="password" 
              placeholder="Enter your password"
              required
            >
          </div>
        </div>
        
        <button type="submit" class="btn-primary" :disabled="isLoading">
          <i v-if="isLoading" class="pi pi-spin pi-spinner"></i>
          <span v-else>Sign In</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f3f4f6;
}

.login-card {
  background: white;
  width: 100%;
  max-width: 400px;
  border-radius: 1rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  padding: 2.5rem 2rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  font-size: 3rem;
  color: #3b82f6;
  margin-bottom: 1rem;
}

.login-header h1 {
  font-size: 1.5rem;
  color: #111827;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.login-header p {
  color: #6b7280;
  margin: 0;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: #9ca3af;
  font-size: 1rem;
}

.input-wrapper input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: #1f2937;
  transition: all 0.2s;
  background-color: white;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.btn-primary {
  width: 100%;
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.875rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
