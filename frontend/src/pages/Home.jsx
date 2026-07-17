import { useEffect, useState } from 'react'
import Footer from '../components/Footer'
import Hero from '../components/Hero'
import NotificationCard from '../components/NotificationCard'
import ServiceCard from '../components/ServiceCard'
import { fetchNotifications } from '../services/api'

const features = [
  'Intent-aware assistant powered by Gemma 4 via Ollama',
  'Knowledge-grounded responses from institutional markdown files',
  'One-click navigation actions for campus service workflows',
]

const services = [
  { title: 'Academics', description: 'Notes, exams, attendance and announcements.', to: '/academics' },
  { title: 'Placements', description: 'Companies, interviews, and career guidance.', to: '/placements' },
  { title: 'Hostel', description: 'Vacancies, rules, complaints and updates.', to: '/hostel' },
  { title: 'Student Support', description: 'Wellness, counseling and emergency help.', to: '/support' },
]

function Home() {
  const [notifications, setNotifications] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    const loadNotifications = async () => {
      try {
        const data = await fetchNotifications()
        setNotifications(data.items ?? [])
      } catch (requestError) {
        setError(requestError.message || 'Could not load notifications.')
      }
    }
    loadNotifications()
  }, [])

  return (
    <main className="mx-auto w-full max-w-7xl px-4 py-6 lg:px-6">
      <Hero />

      <section className="mt-8 rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-xl font-bold text-slate-900">Features</h2>
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-600">
          {features.map((feature) => (
            <li key={feature}>{feature}</li>
          ))}
        </ul>
      </section>

      <section className="mt-8">
        <h2 className="mb-3 text-xl font-bold text-slate-900">Recent Notifications</h2>
        {error && <p className="mb-2 text-sm text-red-600">{error}</p>}
        <div className="grid gap-3 md:grid-cols-3">
          {notifications.map((item) => (
            <NotificationCard key={item.title} title={item.title} detail={item.detail} />
          ))}
        </div>
      </section>

      <section className="mt-8">
        <h2 className="mb-3 text-xl font-bold text-slate-900">Quick Services</h2>
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {services.map((service) => (
            <ServiceCard key={service.title} title={service.title} description={service.description} to={service.to} />
          ))}
        </div>
      </section>

      <Footer />
    </main>
  )
}

export default Home
