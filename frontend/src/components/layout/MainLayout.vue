<script setup>
import Sidebar from './Sidebar.vue'
</script>

<template>
  <div class="layout">
    <Sidebar />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  background-color: #f3f4f6; /* Light gray background for contrast */
  font-family: 'Inter', system-ui, Avenir, Helvetica, Arial, sans-serif;
}
.main-content {
  flex-grow: 1;
  padding: 2.5rem 3rem;
  overflow-y: auto;
  height: 100vh;
  box-sizing: border-box;
}

/* Page Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
