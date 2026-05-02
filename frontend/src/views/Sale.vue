<script setup>
</script>
<template>
  <div class="page">
    <header class="page-header">
      <h1>Point of Sale</h1>
      <div class="status-badge">
        <span class="dot"></span>
        Terminal Active
      </div>
    </header>
    <div class="page-content empty-state">
      <div class="icon-wrapper">
        <i class="pi pi-shopping-cart empty-icon"></i>
      </div>
      <h2>Ready for Sales</h2>
      <p>Scan a barcode or search for products to start a new transaction.</p>
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
.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #dcfce7;
  color: #166534;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-weight: 600;
  font-size: 0.9rem;
}
.dot {
  width: 8px;
  height: 8px;
  background-color: #22c55e;
  border-radius: 50%;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
  100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
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
  background-color: #f3e8ff;
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
  color: #9333ea;
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
