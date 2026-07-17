import ServiceCard from '../components/ServiceCard'

const items = [
  ['Mental Wellness', 'Read student wellbeing resources and tips.'],
  ['Counseling Appointment', 'Book a counseling session from support desk.'],
  ['Anti-Ragging Reporting', 'Escalate anti-ragging issues immediately.'],
  ['Emergency Contacts', 'Quick access to urgent support numbers.'],
]

export default function Support() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Student Support</h1>
      <div className="grid md:grid-cols-2 gap-4">
        {items.map(([title, description]) => <ServiceCard key={title} title={title} description={description} />)}
      </div>
    </div>
  )
}
