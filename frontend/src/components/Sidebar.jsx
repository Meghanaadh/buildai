import { NavLink } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/academics', label: 'Academics' },
  { to: '/placements', label: 'Placements' },
  { to: '/events', label: 'Events' },
  { to: '/hostel', label: 'Hostel' },
  { to: '/support', label: 'Support' },
  { to: '/assistant', label: 'Assistant' },
]

function Sidebar() {
  return (
    <aside className="sticky top-20 hidden h-fit w-56 rounded-xl border border-slate-200 bg-white p-3 lg:block">
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) =>
            `mb-1 block rounded-lg px-3 py-2 text-sm ${
              isActive ? 'bg-teal-100 font-semibold text-teal-800' : 'text-slate-600 hover:bg-slate-100'
            }`
          }
        >
          {link.label}
        </NavLink>
      ))}
    </aside>
  )
}

export default Sidebar
