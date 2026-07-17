import { useEffect, useState } from 'react'
import { fetchModuleData } from '../services/api'

const sections = [
  'Upcoming college events',
  'Hackathons and coding contests',
  'Workshops and training sessions',
  'Club activities and meetups',
]

function Events() {
  const [items, setItems] = useState([])

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchModuleData('events')
        setItems(data.items ?? [])
      } catch {
        setItems([])
      }
    }
    load()
  }, [])

  return (
    <main>
      <h1 className="text-2xl font-bold">Events</h1>
      <ul className="mt-4 list-disc space-y-2 pl-5 text-sm text-slate-700">
        {sections.map((section) => (
          <li key={section}>{section}</li>
        ))}
        {items.map((item) => (
          <li key={item.title}>
            <span className="font-semibold">{item.title}:</span> {item.detail}
          </li>
        ))}
      </ul>
    </main>
  )
}

export default Events
