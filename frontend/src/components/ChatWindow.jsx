import MessageBubble from './MessageBubble'

function ChatWindow({ messages, loading, error, onAction }) {
  return (
    <section className="rounded-xl border border-slate-200 bg-slate-50 p-4">
      <div className="h-[420px] overflow-y-auto pr-1">
        {messages.map((message, index) => (
          <MessageBubble
            key={`${message.role}-${index}`}
            role={message.role}
            content={message.content}
            actions={message.actions}
            onAction={onAction}
          />
        ))}
        {loading && <p className="text-sm text-slate-500">Campus Companion AI is thinking…</p>}
        {error && <p className="text-sm text-red-600">{error}</p>}
      </div>
    </section>
  )
}

export default ChatWindow
