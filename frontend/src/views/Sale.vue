<script setup>
import { ref, onMounted } from 'vue'
import SaleCreateModal from '../components/sales/SaleCreateModal.vue'
import { salesService } from '../services/sales'
import { useToast } from 'primevue/usetoast'

const showCreateModal = ref(false)
const sales = ref([])
const expandedRows = ref([])
const isLoading = ref(true)
const error = ref(null)
const toast = useToast()

const fetchSales = async () => {
  isLoading.value = true
  error.value = null
  try {
    const res = await salesService.getSales()
    sales.value = res.data || res || []
  } catch (err) {
    console.error("Failed to fetch sales", err)
    error.value = 'Failed to load sales data.'
    toast.add({ severity: 'error', summary: 'Error', detail: 'Could not load sales', life: 3000 })
  } finally {
    isLoading.value = false
  }
}

const handleSaleCreated = () => {
  fetchSales()
}

const toggleRow = (id) => {
  const index = expandedRows.value.indexOf(id)
  if (index > -1) {
    expandedRows.value.splice(index, 1)
  } else {
    expandedRows.value.push(id)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

onMounted(() => {
  fetchSales()
})
</script>

<template>
  <div class="page">
    <header class="page-header">
      <h1>Point of Sale</h1>
      <button class="btn-primary" @click="showCreateModal = true">
        <i class="pi pi-plus"></i> Create Sale Invoice
      </button>
    </header>

    <div v-if="isLoading" class="page-content loading-state">
      <i class="pi pi-spin pi-spinner loading-icon"></i>
      <p>Loading sales history...</p>
    </div>

    <div v-else-if="error" class="page-content error-state">
      <i class="pi pi-exclamation-triangle error-icon"></i>
      <p>{{ error }}</p>
      <button @click="fetchSales" class="btn-secondary">Retry</button>
    </div>

    <div v-else-if="sales.length === 0" class="page-content empty-state">
      <div class="icon-wrapper">
        <i class="pi pi-shopping-cart empty-icon"></i>
      </div>
      <h2>Ready for Sales</h2>
      <p>Click "Create Sale Invoice" to start a new transaction.</p>
    </div>

    <div v-else class="page-content table-container">
      <table class="sales-table">
        <thead>
          <tr>
            <th>Invoice ID</th>
            <th>Cashier</th>
            <th>Date</th>
            <th class="text-right">Total Amount</th>
            <th class="text-center">Details</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="sale in sales" :key="sale.id">
            <!-- Main Row -->
            <tr class="main-row" :class="{ 'is-expanded': expandedRows.includes(sale.id) }" @click="toggleRow(sale.id)">
              <td class="font-medium">#INV-{{ sale.id.toString().padStart(4, '0') }}</td>
              <td>
                <span class="user-badge" v-if="sale.user">
                  <i class="pi pi-user"></i> {{ sale.user.username }}
                </span>
                <span v-else class="text-muted">Unknown</span>
              </td>
              <td class="text-muted">{{ formatDate(sale.created_at) }}</td>
              <td class="text-right font-bold text-green">${{ Number(sale.total_amount).toFixed(2) }}</td>
              <td class="text-center">
                <button class="expand-btn">
                  <i class="pi" :class="expandedRows.includes(sale.id) ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
                </button>
              </td>
            </tr>
            
            <!-- Expanded Nested Table -->
            <tr v-if="expandedRows.includes(sale.id)" class="expanded-row">
              <td colspan="5" class="expanded-cell">
                <div class="nested-wrapper">
                  <h4>Items Purchased</h4>
                  <table class="nested-table">
                    <thead>
                      <tr>
                        <th>Product</th>
                        <th class="text-center">Qty</th>
                        <th class="text-right">Unit Price</th>
                        <th class="text-right">Subtotal</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in sale.items" :key="item.id">
                        <td>
                          <div class="product-info">
                            <span class="product-name">{{ item.product?.name || 'Unknown Product' }}</span>
                            <span class="product-sku text-muted">{{ item.product?.sku || 'N/A' }}</span>
                          </div>
                        </td>
                        <td class="text-center text-black">{{ item.quantity }}</td>
                        <td class="text-right text-black">${{ Number(item.unit_price).toFixed(2) }}</td>
                        <td class="text-right font-medium text-black">${{ Number(item.subtotal).toFixed(2) }}</td>
                      </tr>
                    </tbody>
                    <tfoot>
                      <tr>
                        <td colspan="3" class="text-right font-bold text-black">Total</td>
                        <td class="text-right font-bold text-black">${{ Number(sale.total_amount).toFixed(2) }}</td>
                      </tr>
                    </tfoot>
                  </table>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <SaleCreateModal 
      v-if="showCreateModal" 
      @close="showCreateModal = false" 
      @created="handleSaleCreated"
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
  background-color: #9333ea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  box-shadow: 0 4px 6px rgba(147, 51, 234, 0.2);
}

.btn-primary:hover {
  background-color: #7e22ce;
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(1px);
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
  margin-top: 1rem;
}

.btn-secondary:hover {
  background-color: #faf5ff;
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
  background-color: #f3e8ff;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.empty-icon { font-size: 3rem; color: #9333ea; }
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

.table-container {
  overflow-x: auto;
  padding: 0;
}

.sales-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.sales-table th {
  background-color: #f9fafb;
  color: #6b7280;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f3f4f6;
}

.sales-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f3f4f6;
}

.main-row {
  transition: background-color 0.2s;
  cursor: pointer;
}

.main-row:hover {
  background-color: #f9fafb;
}

.main-row.is-expanded {
  background-color: #faf5ff; /* Light purple tint for active row */
  border-left: 3px solid #9333ea;
}

.main-row.is-expanded td:first-child {
  padding-left: calc(1.5rem - 3px);
}

.expanded-cell {
  padding: 0 !important;
  background-color: #f8fafc;
}

.nested-wrapper {
  padding: 1.5rem 2.5rem;
  box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.03);
}

.nested-wrapper h4 {
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
  color: #4b5563;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nested-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.nested-table th {
  background-color: #f1f5f9;
  padding: 0.75rem 1.25rem;
  font-size: 0.8rem;
}

.nested-table td {
  padding: 0.875rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.95rem;
}

.nested-table tr:last-child td {
  border-bottom: none;
}

.user-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background-color: #e0e7ff;
  color: #4338ca;
  padding: 0.25rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 500;
}

.product-info {
  display: flex;
  flex-direction: column;
}

.product-name {
  font-weight: 500;
  color: #111827;
}

.product-sku {
  font-size: 0.8rem;
}

.text-muted { color: #6b7280; }
.font-medium { font-weight: 500; color: #111827; }
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.text-center { text-align: center; }
.text-green { color: #16a34a; }

.expand-btn {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.2s;
}

.main-row:hover .expand-btn {
  color: #9333ea;
  background-color: #f3e8ff;
}
.text-black{
  color: #000;
}
</style>
