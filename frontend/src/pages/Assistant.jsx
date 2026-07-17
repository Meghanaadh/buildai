import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ChatInput from '../components/ChatInput'
import ChatWindow from '../components/ChatWindow'
import { sendChatMessage } from '../services/api'

const initialMessage = {
  role: 'assistant',
  content: 'Hi, I am Campus Companion AI. Ask me anything about academics, hostel, placements, events, or support.',
  actions: [],
}

function Assistant() {
  const [messages, setMessages] = useState([initialMessage])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSend = async (message) => {
    const nextMessages = [...messages, { role: 'user', content: message }]
    setMessages(nextMessages)
    setLoading(true)
    setError('')

    try {
      const response = await sendChatMessage(message, nextMessages)
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: response.reply,
          actions: response.actions ?? [],
        },
      ])
    } catch (requestError) {
      setError(requestError.message || 'Failed to get response from assistant.')
    } finally {
      setLoading(false)
    }
  }

  const handleAction = (route) => {
    if (route) {
      navigate(route)
    }
  }

  return (
    <main>
      <h1 className="text-2xl font-bold text-slate-900">AI Assistant</h1>
      <p className="mt-1 text-sm text-slate-600">Gemma-powered assistant for every campus service.</p>
      <div className="mt-4">
        <ChatWindow messages={messages} loading={loading} error={error} onAction={handleAction} />
        <ChatInput onSend={handleSend} disabled={loading} />
      </div>
    </main>
  )
}

export default Assistant
