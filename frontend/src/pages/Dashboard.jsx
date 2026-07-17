import { useEffect, useState } from 'react'
import NotificationCard from '../components/NotificationCard'
import { fetchDashboardCards } from '../services/api'

function Dashboard() {
  const [cards, setCards] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    const loadCards = async () => {
      try {
        const data = await fetchDashboardCards()
        setCards(data.items ?? [])
      } catch (requestError) {
        setError(requestError.message || 'Could not load dashboard cards.')
      }
    }
    loadCards()
  }, [])

  return (
    <main>
      <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
      <p className="mt-1 text-sm text-slate-600">A quick view of your campus services.</p>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {cards.map((card) => (
          <NotificationCard key={card.title} title={card.title} detail={card.detail} />
        ))}
      </div>
    </main>
  )
}

export default Dashboard
