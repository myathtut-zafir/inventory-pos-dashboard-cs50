<script setup>
import { ref, onMounted } from 'vue'
import { salesService } from '../../services/sales'
import { productsService } from '../../services/products'
import { useToast } from 'primevue/usetoast'

const emit = defineEmits(['close', 'created'])
const toast = useToast()

const items = ref([
  { product_id: '', quantity: 1 }
])
const products = ref([])
const isSubmitting = ref(false)
const isLoadingProducts = ref(true)

const fetchProducts = async () => {
  try {
    const res = await productsService.getProducts()
    products.value = res.data || res || []
  } catch (e) {
    console.error("Failed to load products for sale modal", e)
    toast.add({ severity: 'error', summary: 'Error', detail: 'Could not load products', life: 3000 })
  } finally {
    isLoadingProducts.value = false
  }
}

const isProductSelected = (productId, currentIndex) => {
  return items.value.some((item, index) => index !== currentIndex && item.product_id === productId)
}

const addItem = () => {
  items.value.push({ product_id: '', quantity: 1 })
}

const removeItem = (index) => {
  if (items.value.length > 1) {
    items.value.splice(index, 1)
  }
}

const handleSubmit = async () => {
  // Validate
  const invalidItem = items.value.find(i => !i.product_id || i.quantity <= 0)
  if (invalidItem) {
    toast.add({ severity: 'warn', summary: 'Validation Error', detail: 'Please ensure all items have a selected product and valid quantity.', life: 3000 })
    return
  }

  isSubmitting.value = true
  try {
    const payload = {
      items: items.value.map(item => ({
        product_id: parseInt(item.product_id),
        quantity: parseInt(item.quantity)
      }))
    }
    
    await salesService.createSale(payload)
    toast.add({ severity: 'success', summary: 'Success', detail: 'Sale invoice created successfully!', life: 3000 })
    emit('created')
    emit('close')
  } catch (error) {
    const detailMsg = error.data?.detail || error.data?.message || 'Failed to create sale. Please try again.'
    toast.add({ severity: 'error', summary: 'Error', detail: detailMsg, life: 5000 })
    console.error(error)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchProducts()
})
</script>

<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Create Sale Invoice</h2>
        <button class="close-btn" @click="$emit('close')"><i class="pi pi-times"></i></button>
      </div>

      <div v-if="isLoadingProducts" class="loading-state">
        <i class="pi pi-spin pi-spinner"></i>
        <p>Loading products...</p>
      </div>

      <form v-else @submit.prevent="handleSubmit" class="sale-form">
        
        <div class="items-list">
          <div v-for="(item, index) in items" :key="index" class="item-row">
            <div class="form-group flex-grow">
              <label>Product <span class="required">*</span></label>
              <select v-model="item.product_id" required>
                <option value="" disabled>Select a product...</option>
                <option v-for="product in products" :key="product.id" :value="product.id"
                        :disabled="isProductSelected(product.id, index)"
                        :hidden="isProductSelected(product.id, index)">
                  {{ product.name }} (Stock: {{ product.stock_quantity }}) - ${{ Number(product.price).toFixed(2) }}
                </option>
              </select>
            </div>
            
            <div class="form-group qty-group">
              <label>Qty <span class="required">*</span></label>
              <input type="number" v-model="item.quantity" min="1" required>
            </div>
            
            <button 
              type="button" 
              class="btn-remove" 
              @click="removeItem(index)" 
              v-if="items.length > 1"
              title="Remove item"
            >
              <i class="pi pi-trash"></i>
            </button>
          </div>
        </div>

        <button type="button" class="btn-secondary add-btn" @click="addItem">
          <i class="pi pi-plus"></i> Add Another Item
        </button>

        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="$emit('close')" :disabled="isSubmitting">Cancel</button>
          <button type="submit" class="btn-primary" :disabled="isSubmitting || items.length === 0">
            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
            <span v-else>Submit Sale</span>
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
  max-width: 600px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
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
}

.close-btn:hover { color: #ef4444; }

.loading-state {
  padding: 4rem;
  text-align: center;
  color: #6b7280;
}

.loading-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.sale-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  overflow-y: auto;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-row {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.flex-grow {
  flex-grow: 1;
}

.qty-group {
  width: 80px;
}

label {
  font-size: 0.85rem;
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
  font-size: 0.95rem;
  background-color: white;
  color: #1f2937;
  font-family: inherit;
}

input:focus, select:focus {
  outline: none;
  border-color: #9333ea;
  box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.1);
}

.btn-remove {
  background: none;
  border: none;
  color: #ef4444;
  padding: 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
  height: 42px; /* match input height */
}

.btn-remove:hover {
  background-color: #fef2f2;
}

.add-btn {
  align-self: flex-start;
}

.btn-secondary {
  background-color: white;
  color: #9333ea;
  border: 1px solid #9333ea;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: #faf5ff;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
  border-top: 1px solid #f3f4f6;
  padding-top: 1.5rem;
}

.btn-cancel {
  background: white;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-cancel:hover:not(:disabled) {
  background-color: #f3f4f6;
}

.btn-primary {
  background-color: #9333ea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #7e22ce;
}

.btn-primary:disabled, .btn-cancel:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
