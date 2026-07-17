import ServiceCard from '../components/ServiceCard'

const items = [
  ['Notes', 'Access subject notes and faculty uploads.'],
  ['Exam Schedule', 'View upcoming mid-semester and end-semester exams.'],
  ['Course Registration', 'Track registration windows and submit selections.'],
  ['Attendance', 'Review attendance and escalation workflow.'],
  ['Announcements', 'Academic department updates and deadlines.'],
]

export default function Academics() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Academics</h1>
      <div className="grid md:grid-cols-2 gap-4">
        {items.map(([title, description]) => <ServiceCard key={title} title={title} description={description} />)}
      </div>
    </div>
  )
}
