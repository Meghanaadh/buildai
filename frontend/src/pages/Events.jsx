import ServiceCard from '../components/ServiceCard'

const items = [
  ['Upcoming College Events', 'Discover major academic and cultural events.'],
  ['Hackathons', 'Browse current and upcoming hackathon opportunities.'],
  ['Workshops', 'Register for technical and skill-building workshops.'],
  ['Club Activities', 'Find schedules and updates from student clubs.'],
]

export default function Events() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Events</h1>
      <div className="grid md:grid-cols-2 gap-4">
        {items.map(([title, description]) => <ServiceCard key={title} title={title} description={description} />)}
      </div>
    </div>
  )
}
