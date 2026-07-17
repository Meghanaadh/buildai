const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }

  return response.json()
}

export const chatWithGemma = (message) => request('/chat', {
  method: 'POST',
  body: JSON.stringify({ message }),
})

export const getDashboardData = () => request('/dashboard')
export const getNotifications = () => request('/notifications')
export const getModuleData = (moduleName) => request(`/module/${moduleName}`)
