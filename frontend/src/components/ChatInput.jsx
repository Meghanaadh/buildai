import { useState } from 'react'

function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState('')

  const handleSubmit = (event) => {
    event.preventDefault()
    const trimmed = value.trim()
    if (!trimmed || disabled) {
      return
    }
    onSend(trimmed)
    setValue('')
  }

  return (
    <form className="mt-3 flex gap-2" onSubmit={handleSubmit}>
      <input
        className="flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-400 focus:outline-none"
        onChange={(event) => setValue(event.target.value)}
        placeholder="Ask about academics, hostel, placements, wellness..."
        value={value}
      />
      <button
        className="rounded-lg bg-blue-700 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-400"
        disabled={disabled}
        type="submit"
      >
        Send
      </button>
    </form>
  )
}

export default ChatInput
