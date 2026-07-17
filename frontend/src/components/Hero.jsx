import { Link } from 'react-router-dom'

function Hero() {
  return (
    <section className="rounded-2xl bg-gradient-to-r from-blue-700 to-teal-600 p-8 text-white">
      <p className="text-sm uppercase tracking-wide text-blue-100">AI-first student portal</p>
      <h1 className="mt-2 text-3xl font-bold">One assistant for your entire campus journey</h1>
      <p className="mt-3 max-w-2xl text-blue-50">
        Ask naturally. Campus Companion AI understands your intent, answers from institutional knowledge, and routes
        you to the right service instantly.
      </p>
      <div className="mt-5 flex gap-3">
        <Link className="rounded-lg bg-white px-4 py-2 text-sm font-semibold text-blue-700" to="/assistant">
          Open Assistant
        </Link>
        <Link className="rounded-lg border border-white/60 px-4 py-2 text-sm font-semibold text-white" to="/dashboard">
          View Dashboard
        </Link>
      </div>
    </section>
  )
}

export default Hero
