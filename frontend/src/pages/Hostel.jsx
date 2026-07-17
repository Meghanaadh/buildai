import ServiceCard from '../components/ServiceCard'

const items = [
  ['Nearby Hostels', 'Compare available nearby hostel options.'],
  ['Vacant Rooms', 'View current room availability and waitlist status.'],
  ['Hostel Rules', 'Read conduct and discipline requirements.'],
  ['Hostel Complaints', 'Submit room and utility complaints quickly.'],
]

export default function Hostel() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Hostel</h1>
      <div className="grid md:grid-cols-2 gap-4">
        {items.map(([title, description]) => <ServiceCard key={title} title={title} description={description} />)}
      </div>
    </div>
  )
}
