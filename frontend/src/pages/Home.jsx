import { useEffect, useState } from 'react'
import Hero from '../components/Hero'
import NotificationCard from '../components/NotificationCard'
import ServiceCard from '../components/ServiceCard'
import { getNotifications } from '../services/api'

const features = [
  ['AI-first Portal', 'Use Gemma as the primary interface for all campus services.'],
  ['Intent-based Routing', 'Queries are classified and routed to the right module.'],
  ['No Policy Hallucination', 'Unknown policy queries are escalated to departments.'],
  ['Student Support', 'Guidance, counseling navigation, and emergency support flows.'],
]

export default function Home() {
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    getNotifications().then((data) => setNotifications(data.items)).catch(() => setNotifications([]))
  }, [])

  return (
    <div className="space-y-6">
      <Hero />
      <section>
        <h2 className="text-xl font-semibold text-slate-800 mb-3">Features</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {features.map(([title, description]) => (
            <ServiceCard key={title} title={title} description={description} />
          ))}
        </div>
      </section>
      <section>
        <h2 className="text-xl font-semibold text-slate-800 mb-3">Recent Notifications</h2>
        <ul className="space-y-2">
          {notifications.map((notification) => (
            <NotificationCard key={notification} text={notification} />
          ))}
        </ul>
      </section>
    </div>
  )
}
