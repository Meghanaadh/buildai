const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

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

export const sendChatMessage = (message, history = []) => request('/chat', {
  method: 'POST',
  body: JSON.stringify({ message, history }),
})

export const chatWithGemma = sendChatMessage
export const getDashboardCards = () => request('/dashboard/cards')
export const getNotifications = () => request('/notifications')
export const getModuleData = (moduleName) => request(`/modules/${moduleName}`)
