import { useEffect, useState } from 'react'
import { fetchModuleData } from '../services/api'

const sections = [
  'Nearby hostels and commute details',
  'Vacancy updates and room availability',
  'Hostel rules and expected conduct',
  'Complaint and grievance submissions',
]

function Hostel() {
  const [items, setItems] = useState([])

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchModuleData('hostel')
        setItems(data.items ?? [])
      } catch {
        setItems([])
      }
    }
    load()
  }, [])

  return (
    <main>
      <h1 className="text-2xl font-bold">Hostel</h1>
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

export default Hostel
