<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
} from 'chart.js'
import { Bar, Pie } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement)

const barData = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June'],
  datasets: [
    {
      label: 'Monthly Sales ($)',
      backgroundColor: '#3b82f6',
      borderRadius: 6,
      data: [1200, 1900, 1500, 2200, 1800, 2800]
    }
  ]
}

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: '#f3f4f6'
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
}

const pieData = {
  labels: ['Electronics', 'Clothing', 'Groceries', 'Books'],
  datasets: [
    {
      backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
      borderWidth: 0,
      data: [45, 25, 20, 10]
    }
  ]
}

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 20
      }
    }
  }
}
</script>

<template>
  <div class="page">
    <header class="page-header">
      <h1>Dashboard</h1>
      <div class="date-picker">
        <i class="pi pi-calendar"></i> Today: {{ new Date().toLocaleDateString() }}
      </div>
    </header>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-info">
          <h3>Total Sales</h3>
          <p class="value">$12,450</p>
        </div>
        <div class="stat-icon bg-blue">
          <i class="pi pi-dollar"></i>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>Total Orders</h3>
          <p class="value">150</p>
        </div>
        <div class="stat-icon bg-green">
          <i class="pi pi-shopping-cart"></i>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>Products Sold</h3>
          <p class="value">345</p>
        </div>
        <div class="stat-icon bg-orange">
          <i class="pi pi-box"></i>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <h3>Sales Overview</h3>
        <div class="chart-container">
          <Bar :data="barData" :options="barOptions" />
        </div>
      </div>
      <div class="chart-card">
        <h3>Sales by Category</h3>
        <div class="chart-container">
          <Pie :data="pieData" :options="pieOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
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
.date-picker {
  background: white;
  padding: 0.6rem 1.25rem;
  border-radius: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4b5563;
  font-weight: 600;
  font-size: 0.95rem;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s;
}
.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.stat-info h3 {
  margin: 0;
  font-size: 1.05rem;
  color: #6b7280;
  font-weight: 600;
}
.stat-info .value {
  margin: 0.5rem 0 0 0;
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}
.stat-icon {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}
.bg-blue { background-color: #eff6ff; color: #3b82f6; }
.bg-green { background-color: #f0fdf4; color: #22c55e; }
.bg-orange { background-color: #fff7ed; color: #f97316; }

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}
@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
.chart-card {
  background: white;
  padding: 1.75rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.chart-card h3 {
  margin: 0 0 1.5rem 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>
