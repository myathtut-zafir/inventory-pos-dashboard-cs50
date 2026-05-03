<script setup>
import Toast from 'primevue/toast'
</script>

<template>
  <Toast />
  <router-view />
</template>

<style>
/* Reset basic styles globally since this is the root component */
body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #f3f4f6;
}
* {
  box-sizing: border-box;
}
</style>
