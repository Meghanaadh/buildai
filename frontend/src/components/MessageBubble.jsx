export default function MessageBubble({ role, text, action, onAction }) {
  const isUser = role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[80%] rounded-xl p-3 text-sm ${isUser ? 'bg-blue-700 text-white' : 'bg-white border border-slate-200 text-slate-800'}`}>
        <p className="whitespace-pre-wrap">{text}</p>
        {!isUser && action?.route && (
          <button
            onClick={() => onAction(action.route)}
            className="mt-3 text-xs bg-teal-600 text-white px-3 py-1.5 rounded-md"
          >
            {action.label}
          </button>
        )}
      </div>
    </div>
  )
}
