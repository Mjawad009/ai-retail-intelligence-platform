import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { BarChart3, TrendingUp, AlertTriangle, MessageCircle, Home } from 'lucide-react'

import Dashboard from './pages/Dashboard'
import Forecasting from './pages/Forecasting'
import InventoryRisk from './pages/InventoryRisk'
import Assistant from './pages/Assistant'

function App() {
  const [sidebarOpen, setSidebarOpen] = React.useState(true)

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-gray-900 text-white transition-all duration-300 shadow-lg`}>
          <div className="p-4 flex items-center justify-between">
            {sidebarOpen && <h1 className="text-xl font-bold">Retail AI</h1>}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-1 hover:bg-gray-800 rounded"
            >
              ☰
            </button>
          </div>

          <nav className="space-y-2 p-4">
            <NavLink icon={<Home />} label="Dashboard" to="/" sidebarOpen={sidebarOpen} />
            <NavLink icon={<TrendingUp />} label="Forecasting" to="/forecasting" sidebarOpen={sidebarOpen} />
            <NavLink icon={<AlertTriangle />} label="Inventory" to="/inventory" sidebarOpen={sidebarOpen} />
            <NavLink icon={<MessageCircle />} label="Assistant" to="/assistant" sidebarOpen={sidebarOpen} />
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Top Bar */}
          <div className="bg-white shadow px-6 py-4">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold text-gray-800">AI Retail Intelligence</h2>
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-600">Version 1.0</span>
              </div>
            </div>
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-auto p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/forecasting" element={<Forecasting />} />
              <Route path="/inventory" element={<InventoryRisk />} />
              <Route path="/assistant" element={<Assistant />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  )
}

const NavLink = ({ icon, label, to, sidebarOpen }) => {
  return (
    <Link
      to={to}
      className="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-gray-800 transition text-gray-300 hover:text-white"
    >
      {icon}
      {sidebarOpen && <span>{label}</span>}
    </Link>
  )
}

export default App
