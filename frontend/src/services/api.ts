import axios from 'axios'

/** Public Render API — used when VITE_API_URL is missing at build time (common on first deploy). */
const RENDER_API_BASE = 'https://diet-recommendation-api.onrender.com/api/v1'

export const API_BASE =
  import.meta.env.VITE_API_URL ||
  (import.meta.env.PROD ? RENDER_API_BASE : '/api/v1')

export const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)
