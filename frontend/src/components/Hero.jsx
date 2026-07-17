import { Link } from 'react-router-dom'

export default function Hero() {
  return (
    <section className="bg-gradient-to-r from-blue-700 to-teal-600 text-white rounded-xl p-8">
      <h1 className="text-3xl md:text-4xl font-bold mb-3">One AI Entry Point for Campus Life</h1>
      <p className="text-blue-50 max-w-2xl mb-6">
        Ask Gemma about academics, placements, hostel services, events, administration, grievances, and wellness.
      </p>
      <Link to="/assistant" className="inline-flex bg-white text-blue-700 font-semibold px-4 py-2 rounded-lg">
        Open AI Assistant
      </Link>
    </section>
  )
}
