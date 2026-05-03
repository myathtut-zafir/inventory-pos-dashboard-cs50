import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Products from '../views/Products.vue'
import Sale from '../views/Sale.vue'
import Users from '../views/Users.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/products',
      name: 'products',
      component: Products
    },
    {
      path: '/sale',
      name: 'sale',
      component: Sale
    },
    {
      path: '/users',
      name: 'users',
      component: Users
    }
  ]
})

export default router
