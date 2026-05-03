<script setup>
import { ref, onMounted } from 'vue'
import { productsService } from '../services/products'
import ProductCreateModal from '../components/products/ProductCreateModal.vue'

const products = ref([])
const isLoading = ref(true)
const error = ref(null)
const showCreateModal = ref(false)

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

const handleProductCreated = () => {
  fetchProducts() // Refresh list after creation
}

onMounted(() => {
  fetchProducts()
})
</script>
<template>
  <div class="page">
    <header class="page-header">
      <h1>Products</h1>
      <button class="btn-primary" @click="showCreateModal = true">
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

    <div v-else class="page-content table-container">
      <table class="products-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>SKU</th>
            <th>Quantity</th>
            <th>Price</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td class="text-muted">#{{ product.id }}</td>
            <td class="font-medium">{{ product.name }}</td>
            <td class="text-muted">{{ product.sku }}</td>
            <td>
              <span class="quantity-badge" :class="{'low-stock': product.stock_quantity < 10}">
                {{ product.stock_quantity }}
              </span>
            </td>
            <td class="font-semibold">${{ Number(product.price).toFixed(2) }}</td>
            <td class="text-right">
              <button class="action-btn"><i class="pi pi-pencil"></i></button>
              <button class="action-btn danger"><i class="pi pi-trash"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <ProductCreateModal 
      v-if="showCreateModal" 
      @close="showCreateModal = false" 
      @created="handleProductCreated"
    />
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

.table-container {
  overflow-x: auto;
  padding: 0;
}
.products-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.products-table th,
.products-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f3f4f6;
}
.products-table th {
  background-color: #f9fafb;
  color: #6b7280;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  position: sticky;
  top: 0;
}
.products-table tbody tr {
  transition: background-color 0.2s;
}
.products-table tbody tr:hover {
  background-color: #f9fafb;
}
.text-muted { color: #6b7280; }
.font-medium { font-weight: 500; color: #111827; }
.font-semibold { font-weight: 600; color: #111827; }
.text-right { text-align: right; }
.quantity-badge {
  background-color: #dcfce7;
  color: #166534;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
}
.quantity-badge.low-stock {
  background-color: #fee2e2;
  color: #991b1b;
}
.action-btn {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
}
.action-btn:hover {
  color: #3b82f6;
  background-color: #eff6ff;
}
.action-btn.danger:hover {
  color: #ef4444;
  background-color: #fef2f2;
}
</style>
