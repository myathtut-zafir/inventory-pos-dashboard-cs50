<script setup>
import { ref, onMounted } from 'vue'
import { productsService } from '../services/products'

const products = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchProducts = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await productsService.getProducts()
    // Backend might return the array directly or wrapped in a 'data' property
    products.value = response.data || response || []
  } catch (err) {
    error.value = 'Failed to load products. Please make sure the backend is running.'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchProducts()
})
</script>
<template>
  <div class="page">
    <header class="page-header">
      <h1>Products</h1>
      <button class="btn-primary">
        <i class="pi pi-plus"></i> Add Product
      </button>
    </header>
    
    <div v-if="isLoading" class="page-content loading-state">
      <i class="pi pi-spin pi-spinner loading-icon"></i>
      <p>Loading products...</p>
    </div>
    
    <div v-else-if="error" class="page-content error-state">
      <i class="pi pi-exclamation-triangle error-icon"></i>
      <p>{{ error }}</p>
      <button @click="fetchProducts" class="btn-secondary">Retry</button>
    </div>

    <div v-else-if="products.length === 0" class="page-content empty-state">
      <div class="icon-wrapper">
        <i class="pi pi-box empty-icon"></i>
      </div>
      <h2>No Products Found</h2>
      <p>You haven't added any products to your inventory yet.</p>
    </div>

    <div v-else class="page-content products-grid">
      <div v-for="product in products" :key="product.id || product" class="product-card">
         <div class="product-info">
           <h3>{{ product.name || 'Unnamed Product' }}</h3>
           <p class="sku">{{ product.sku || 'No SKU' }}</p>
         </div>
         <p class="price">{{ product.price ? '$' + product.price : 'N/A' }}</p>
      </div>
    </div>
  </div>
</template>
<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  height: 100%;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.page-header h1 {
  font-size: 2.25rem;
  color: #111827;
  margin: 0;
  font-weight: 700;
}
.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
}
.btn-primary:hover {
  background-color: #2563eb;
  transform: translateY(-1px);
}
.btn-primary:active {
  transform: translateY(1px);
}
.btn-secondary {
  background-color: white;
  color: #3b82f6;
  border: 1px solid #3b82f6;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 1rem;
}
.btn-secondary:hover {
  background-color: #eff6ff;
}
.page-content {
  background: white;
  border-radius: 1rem;
  flex-grow: 1;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
.empty-state, .loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 4rem;
}
.icon-wrapper {
  background-color: #eff6ff;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}
.empty-icon { font-size: 3rem; color: #3b82f6; }
.loading-icon { font-size: 3rem; color: #9ca3af; margin-bottom: 1rem; }
.error-icon { font-size: 3rem; color: #ef4444; margin-bottom: 1rem; }

.empty-state h2 {
  color: #1f2937;
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}
.empty-state p, .loading-state p, .error-state p {
  color: #6b7280;
  margin: 0;
  font-size: 1.1rem;
}
.error-state p { color: #ef4444; }

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 2rem;
  background: transparent;
  box-shadow: none;
  align-items: flex-start;
  align-content: flex-start;
}
.product-card {
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.product-info h3 {
  margin: 0 0 0.25rem 0;
  color: #1f2937;
  font-size: 1.1rem;
}
.product-info .sku {
  margin: 0;
  color: #9ca3af;
  font-size: 0.9rem;
}
.price {
  font-weight: 700;
  color: #10b981;
  font-size: 1.25rem;
  margin: 0;
}
</style>
