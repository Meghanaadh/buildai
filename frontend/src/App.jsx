import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import Footer from './components/Footer'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Academics from './pages/Academics'
import Assistant from './pages/Assistant'
import Dashboard from './pages/Dashboard'
import Events from './pages/Events'
import Home from './pages/Home'
import Hostel from './pages/Hostel'
import Placements from './pages/Placements'
import Support from './pages/Support'

function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-slate-100">
      <Navbar />
      <div className="flex-1 max-w-7xl w-full mx-auto md:flex">
        <Sidebar />
        <main className="flex-1 p-6">{children}</main>
      </div>
      <Footer />
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout><Home /></Layout>} />
        <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
        <Route path="/assistant" element={<Layout><Assistant /></Layout>} />
        <Route path="/academics" element={<Layout><Academics /></Layout>} />
        <Route path="/placements" element={<Layout><Placements /></Layout>} />
        <Route path="/events" element={<Layout><Events /></Layout>} />
        <Route path="/hostel" element={<Layout><Hostel /></Layout>} />
        <Route path="/support" element={<Layout><Support /></Layout>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
