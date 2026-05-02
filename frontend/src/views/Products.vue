<script setup>
</script>
<template>
  <div class="page">
    <header class="page-header">
      <h1>Products</h1>
      <button class="btn-primary">
        <i class="pi pi-plus"></i> Add Product
      </button>
    </header>
    <div class="page-content empty-state">
      <div class="icon-wrapper">
        <i class="pi pi-box empty-icon"></i>
      </div>
      <h2>No Products Found</h2>
      <p>You haven't added any products to your inventory yet.</p>
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
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 1rem;
  flex-grow: 1;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
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
.empty-icon {
  font-size: 3rem;
  color: #3b82f6;
}
.empty-state h2 {
  color: #1f2937;
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}
.empty-state p {
  color: #6b7280;
  margin: 0;
  font-size: 1.1rem;
}
</style>
