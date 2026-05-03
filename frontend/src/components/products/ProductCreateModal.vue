<script setup>
import { ref } from 'vue'
import { productsService } from '../../services/products'
import { useToast } from 'primevue/usetoast'

const emit = defineEmits(['close', 'created'])
const toast = useToast()

const formData = ref({
  sku: '',
  name: '',
  price: '',
  stock_quantity: 0
})

const isSubmitting = ref(false)
const errorMessage = ref('')

const handleSubmit = async () => {
  isSubmitting.value = true
  errorMessage.value = ''
  
  try {
    const payload = {
      ...formData.value,
      price: String(formData.value.price) // API expects a string based on previous response
    }
    await productsService.createProduct(payload)
    toast.add({ severity: 'success', summary: 'Success', detail: 'Product created successfully', life: 3000 })
    emit('created') // Notify parent to refresh list
    emit('close')   // Close the modal
  } catch (error) {
    const detailMsg = error.data?.detail || error.data?.message || 'Failed to create product. Please try again.'
    errorMessage.value = detailMsg
    toast.add({ severity: 'error', summary: 'Error', detail: detailMsg, life: 5000 })
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
        <h2>Add New Product</h2>
        <button class="close-btn" @click="$emit('close')"><i class="pi pi-times"></i></button>
      </div>

      <form @submit.prevent="handleSubmit" class="product-form">
        <div v-if="errorMessage" class="error-banner">
          {{ errorMessage }}
        </div>

        <div class="form-group">
          <label for="sku">SKU <span class="required">*</span></label>
          <input 
            type="text" 
            id="sku" 
            v-model="formData.sku" 
            required 
            placeholder="e.g. BEV-COKE-330"
          >
        </div>

        <div class="form-group">
          <label for="name">Product Name <span class="required">*</span></label>
          <input 
            type="text" 
            id="name" 
            v-model="formData.name" 
            required 
            placeholder="e.g. Coca-Cola 330ml"
          >
        </div>

        <div class="form-row">
          <div class="form-group half">
            <label for="price">Price ($) <span class="required">*</span></label>
            <input 
              type="number" 
              step="0.01" 
              id="price" 
              v-model="formData.price" 
              required 
              placeholder="0.00"
            >
          </div>

          <div class="form-group half">
            <label for="stock_quantity">Stock Quantity <span class="required">*</span></label>
            <input 
              type="number" 
              id="stock_quantity" 
              v-model="formData.stock_quantity" 
              required
              min="0"
            >
          </div>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="$emit('close')" :disabled="isSubmitting">Cancel</button>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
            <span v-else>Save Product</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
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
  max-width: 500px;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s ease-out;
  overflow: hidden;
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
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #ef4444;
}

.product-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.error-banner {
  background-color: #fef2f2;
  color: #991b1b;
  padding: 1rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  border-left: 4px solid #ef4444;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.half {
  flex: 1;
}

label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
}

.required {
  color: #ef4444;
  margin-left: 0.1rem;
}

input {
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: #1f2937;
  background-color: white;
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}

input:focus {
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
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
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
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
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
