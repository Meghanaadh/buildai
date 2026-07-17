import { NavLink } from 'react-router-dom'

const links = [
  ['Dashboard', '/dashboard'],
  ['Assistant', '/assistant'],
  ['Academics', '/academics'],
  ['Placements', '/placements'],
  ['Events', '/events'],
  ['Hostel', '/hostel'],
  ['Support', '/support'],
]

export default function Sidebar() {
  return (
    <aside className="w-full md:w-64 bg-white border-r border-slate-200 p-4">
      <nav className="flex md:flex-col gap-2 overflow-x-auto">
        {links.map(([label, path]) => (
          <NavLink
            key={path}
            to={path}
            className={({ isActive }) =>
              `px-3 py-2 rounded-md text-sm font-medium whitespace-nowrap ${
                isActive ? 'bg-teal-100 text-teal-800' : 'hover:bg-slate-100 text-slate-700'
              }`
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
