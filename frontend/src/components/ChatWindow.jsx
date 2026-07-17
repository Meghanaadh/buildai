import MessageBubble from './MessageBubble'

export default function ChatWindow({ messages, onAction }) {
  return (
    <section className="bg-slate-50 border border-slate-200 rounded-xl p-4 min-h-[420px] max-h-[520px] overflow-y-auto space-y-3">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          role={message.role}
          text={message.text}
          action={message.action}
          onAction={onAction}
        />
      ))}
    </section>
  )
}
