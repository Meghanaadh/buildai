import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ChatInput from '../components/ChatInput'
import ChatWindow from '../components/ChatWindow'
import { chatWithGemma } from '../services/api'

export default function Assistant() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      text: 'Hi! I am Gemma, your Campus Companion. Ask me about academics, placements, hostel, events, support, or grievances.',
    },
  ])

  const send = async (text) => {
    const userMessage = { id: Date.now(), role: 'user', text }
    setMessages((prev) => [...prev, userMessage])
    setLoading(true)

    try {
      const response = await chatWithGemma(text)
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          text: response.answer,
          action: response.action,
        },
      ])
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          text: 'I am unable to reach the campus AI service right now. Please try again shortly.',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">AI Assistant</h1>
      <ChatWindow messages={messages} onAction={navigate} />
      <ChatInput onSend={send} loading={loading} />
    </div>
  )
}
