const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const parseError = async (response) => {
  try {
    const payload = await response.json()
    return payload.detail || 'Request failed'
  } catch {
    return 'Request failed'
  }
}

export const sendChatMessage = async (message, history = []) => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history }),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json()
}

export const fetchDashboardCards = async () => {
  const response = await fetch(`${API_BASE_URL}/dashboard/cards`)
  if (!response.ok) {
    throw new Error(await parseError(response))
  }
  return response.json()
}

export const fetchNotifications = async () => {
  const response = await fetch(`${API_BASE_URL}/notifications`)
  if (!response.ok) {
    throw new Error(await parseError(response))
  }
  return response.json()
}

export const fetchModuleData = async (moduleName) => {
  const response = await fetch(`${API_BASE_URL}/modules/${moduleName}`)
  if (!response.ok) {
    throw new Error(await parseError(response))
  }
  return response.json()
}
