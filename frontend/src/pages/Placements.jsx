import ServiceCard from '../components/ServiceCard'

const items = [
  ['Placement Notifications', 'Company drives, eligibility, and deadlines.'],
  ['Upcoming Companies', 'See upcoming recruiters and role details.'],
  ['Resume Tips', 'Improve your resume with placement-cell guidance.'],
  ['Mock Interview Registration', 'Register for practice interview slots.'],
  ['Career Guidance', 'Access mentors and career roadmap support.'],
]

export default function Placements() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Placements</h1>
      <div className="grid md:grid-cols-2 gap-4">
        {items.map(([title, description]) => <ServiceCard key={title} title={title} description={description} />)}
      </div>
    </div>
  )
}
