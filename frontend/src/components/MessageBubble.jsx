function MessageBubble({ role, content, actions = [], onAction }) {
  const isUser = role === 'user'
  return (
    <div className={`mb-3 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
          isUser ? 'bg-blue-700 text-white' : 'bg-white text-slate-800 border border-slate-200'
        }`}
      >
        <p className="whitespace-pre-wrap">{content}</p>
        {!isUser && actions.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {actions.map((action) => (
              <button
                key={action.label}
                className="rounded-md bg-teal-100 px-3 py-1 text-xs font-semibold text-teal-800 hover:bg-teal-200"
                onClick={() => onAction(action.route)}
                type="button"
              >
                {action.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
