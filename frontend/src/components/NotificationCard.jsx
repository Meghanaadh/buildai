function NotificationCard({ title, detail }) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h4 className="font-semibold text-slate-900">{title}</h4>
      <p className="mt-1 text-sm text-slate-600">{detail}</p>
    </article>
  )
}

export default NotificationCard
