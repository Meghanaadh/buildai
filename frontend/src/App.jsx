import { Navigate, Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Assistant from './pages/Assistant'
import Academics from './pages/Academics'
import Placements from './pages/Placements'
import Events from './pages/Events'
import Hostel from './pages/Hostel'
import Support from './pages/Support'

const withShell = (Page) => (
  <div className="mx-auto flex w-full max-w-7xl gap-4 px-4 py-6 lg:px-6">
    <Sidebar />
    <div className="min-w-0 flex-1">
      <Page />
    </div>
  </div>
)

function App() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={withShell(Dashboard)} />
        <Route path="/assistant" element={withShell(Assistant)} />
        <Route path="/academics" element={withShell(Academics)} />
        <Route path="/placements" element={withShell(Placements)} />
        <Route path="/events" element={withShell(Events)} />
        <Route path="/hostel" element={withShell(Hostel)} />
        <Route path="/support" element={withShell(Support)} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  )
}

export default App
