import { useEffect, useState } from 'react'
import { fetchModuleData } from '../services/api'

const sections = ['Notes and learning resources', 'Attendance information', 'Academic announcements']

function Academics() {
  const [items, setItems] = useState([])

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchModuleData('academics')
        setItems(data.items ?? [])
      } catch {
        setItems([])
      }
    }
    load()
  }, [])

  return (
    <main>
      <h1 className="text-2xl font-bold">Academics</h1>
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

export default Academics
