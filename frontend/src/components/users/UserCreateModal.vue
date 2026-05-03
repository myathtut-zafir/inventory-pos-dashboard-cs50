<script setup>
import { ref } from 'vue'
import { usersService } from '../../services/users'
import { useToast } from 'primevue/usetoast'

const emit = defineEmits(['close', 'created'])

const username = ref('')
const password = ref('')
const role = ref('staff') // default role
const isSubmitting = ref(false)
const toast = useToast()

const handleSubmit = async () => {
  isSubmitting.value = true
  
  const payload = {
    username: username.value,
    password: password.value,
    role: role.value
  }

  try {
    await usersService.createUser(payload)
    toast.add({ severity: 'success', summary: 'Success', detail: 'User registered successfully', life: 3000 })
    emit('created')
    emit('close')
  } catch (error) {
    let detailMsg = 'Failed to register user. Please try again.'
    
    if (Array.isArray(error.data?.detail)) {
      // Handle FastAPI Pydantic validation error array
      detailMsg = error.data.detail.map(err => err.msg).join(', ')
    } else if (error.data?.detail) {
      // Handle standard string detail
      detailMsg = error.data.detail
    } else if (error.data?.message) {
      detailMsg = error.data.message
    }

    toast.add({ severity: 'error', summary: 'Validation Error', detail: detailMsg, life: 5000 })
    console.error(error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Register New User</h2>
        <button class="close-btn" @click="$emit('close')"><i class="pi pi-times"></i></button>
      </div>

      <form @submit.prevent="handleSubmit" class="user-form">
        <div class="form-group">
          <label for="username">Username <span class="required">*</span></label>
          <input type="text" id="username" v-model="username" required placeholder="e.g. jdoe123">
        </div>

        <div class="form-group">
          <label for="password">Password <span class="required">*</span></label>
          <input type="password" id="password" v-model="password" required placeholder="Enter a secure password">
        </div>

        <div class="form-group">
          <label for="role">Role <span class="required">*</span></label>
          <select id="role" v-model="role" required>
            <option value="staff">Staff</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="$emit('close')" :disabled="isSubmitting">Cancel</button>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
            <span v-else>Register User</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Modal Base Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 450px;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f3f4f6;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #111827;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.25rem;
  cursor: pointer;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #ef4444;
}

.user-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
}

.required {
  color: #ef4444;
}

input, select {
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: #1f2937;
  transition: all 0.2s;
  background-color: white;
  font-family: inherit;
}

input:focus, select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-cancel {
  background: white;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover:not(:disabled) {
  background-color: #f3f4f6;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-primary:disabled, .btn-cancel:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
