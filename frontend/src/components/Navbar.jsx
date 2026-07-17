import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <header className="bg-blue-700 text-white px-6 py-4 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        <Link to="/" className="font-semibold text-xl">Campus Companion AI</Link>
        <span className="text-sm text-blue-100">Gemma 4 Powered Student Portal</span>
      </div>
    </header>
  )
}
