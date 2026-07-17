import { useEffect, useState } from 'react'
import ServiceCard from '../components/ServiceCard'
import { getDashboardCards } from '../services/api'

export default function Dashboard() {
  const [cards, setCards] = useState([])

  useEffect(() => {
    getDashboardCards().then((data) => setCards(data.items ?? [])).catch(() => setCards([]))
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Dashboard</h1>
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {cards.map((card) => (
          <ServiceCard key={card.title} title={card.title} description={card.detail} />
        ))}
      </div>
    </div>
  )
}
