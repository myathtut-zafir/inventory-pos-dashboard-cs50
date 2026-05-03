<script setup>
import { ref, onMounted } from 'vue'
import { usersService } from '../services/users'
import UserCreateModal from '../components/users/UserCreateModal.vue'

const users = ref([])
const isLoading = ref(true)
const error = ref(null)
const showCreateModal = ref(false)

const fetchUsers = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await usersService.getUsers()
    users.value = response.data || response || []
  } catch (err) {
    error.value = 'Failed to load users. Please make sure the backend is running.'
    console.error(err)
  } finally {
    isLoading.value = false
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
  fetchUsers()
})
</script>

<template>
  <div class="page">
    <header class="page-header">
      <h1>Users</h1>
      <button class="btn-primary" @click="showCreateModal = true">
        <i class="pi pi-plus"></i> Add User
      </button>
    </header>
    
    <div v-if="isLoading" class="page-content loading-state">
      <i class="pi pi-spin pi-spinner loading-icon"></i>
      <p>Loading users...</p>
    </div>
    
    <div v-else-if="error" class="page-content error-state">
      <i class="pi pi-exclamation-triangle error-icon"></i>
      <p>{{ error }}</p>
      <button @click="fetchUsers" class="btn-secondary">Retry</button>
    </div>

    <div v-else-if="users.length === 0" class="page-content empty-state">
      <div class="icon-wrapper">
        <i class="pi pi-users empty-icon"></i>
      </div>
      <h2>No Users Found</h2>
      <p>There are currently no users in the system.</p>
    </div>

    <div v-else class="page-content table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Role</th>
            <th>Created At</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="text-muted">#{{ user.id }}</td>
            <td class="font-medium">{{ user.username }}</td>
            <td>
              <span class="role-badge" :class="user.role?.toLowerCase()">
                {{ user.role }}
              </span>
            </td>
            <td class="text-muted">{{ formatDate(user.created_at) }}</td>
            <td class="text-right">
              <button class="action-btn"><i class="pi pi-pencil"></i></button>
              <button class="action-btn danger"><i class="pi pi-trash"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <UserCreateModal 
      v-if="showCreateModal" 
      @close="showCreateModal = false" 
      @created="fetchUsers"
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
.users-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.users-table th,
.users-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f3f4f6;
}
.users-table th {
  background-color: #f9fafb;
  color: #6b7280;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  position: sticky;
  top: 0;
}
.users-table tbody tr {
  transition: background-color 0.2s;
}
.users-table tbody tr:hover {
  background-color: #f9fafb;
}
.text-muted { color: #6b7280; }
.font-medium { font-weight: 500; color: #111827; }
.text-right { text-align: right; }

.role-badge {
  background-color: #f3f4f6;
  color: #4b5563;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: capitalize;
}
.role-badge.admin {
  background-color: #dcfce7;
  color: #166534;
}
.role-badge.staff, .role-badge.manager {
  background-color: #dbeafe;
  color: #1e40af;
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
