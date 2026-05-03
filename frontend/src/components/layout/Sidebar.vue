<script setup>
</script>

<template>
  <aside class="sidebar">
    <div class="logo">
      <h2>POS System</h2>
    </div>
    <nav class="menu">
      <router-link to="/" class="menu-item" active-class="active">
        <i class="pi pi-home"></i> Dashboard
      </router-link>
      <router-link to="/products" class="menu-item" active-class="active">
        <i class="pi pi-box"></i> Products
      </router-link>
      <router-link to="/users" class="menu-item" active-class="active">
        <i class="pi pi-users"></i> Users
      </router-link>
      <router-link to="/sale" class="menu-item" active-class="active">
        <i class="pi pi-shopping-cart"></i> Sale
      </router-link>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 280px;
  background-color: #111827;
  color: #ffffff;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
}
.logo {
  padding: 2.5rem 2rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.logo h2 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #3b82f6; /* Blue accent */
  letter-spacing: 0.5px;
}
.menu {
  display: flex;
  flex-direction: column;
  padding: 2rem 1.5rem;
  gap: 0.75rem;
}
.menu-item {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1rem 1.5rem;
  color: #9ca3af;
  text-decoration: none;
  border-radius: 0.75rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 500;
  font-size: 1.05rem;
}
.menu-item:hover {
  background-color: rgba(59, 130, 246, 0.1);
  color: #ffffff;
  transform: translateX(5px);
}
.menu-item.active {
  background-color: #3b82f6;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}
.menu-item i {
  font-size: 1.25rem;
}
</style>
