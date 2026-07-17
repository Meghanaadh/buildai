import { Link } from 'react-router-dom'

function ServiceCard({ title, description, to }) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="font-semibold text-slate-900">{title}</h3>
      <p className="mt-1 text-sm text-slate-600">{description}</p>
      <Link className="mt-3 inline-block text-sm font-semibold text-teal-700" to={to}>
        Open module →
      </Link>
    </article>
  )
}

export default ServiceCard
