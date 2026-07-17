import { useState } from 'react'

export default function ChatInput({ onSend, loading }) {
  const [message, setMessage] = useState('')

  const submit = (event) => {
    event.preventDefault()
    const trimmed = message.trim()
    if (!trimmed || loading) return
    onSend(trimmed)
    setMessage('')
  }

  return (
    <form onSubmit={submit} className="mt-4 flex gap-2">
      <input
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        placeholder="Ask Gemma anything about campus services..."
        className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm"
      />
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-700 text-white px-4 py-2 rounded-lg text-sm disabled:opacity-60"
      >
        {loading ? 'Sending...' : 'Send'}
      </button>
    </form>
  )
}
