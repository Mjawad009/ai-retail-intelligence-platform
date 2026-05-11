import React from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts'
import { AlertCircle, TrendingUp, Package, Eye, Clock } from 'lucide-react'

const Dashboard = () => {
  const [summary, setSummary] = React.useState(null)
  const [salesTrends, setSalesTrends] = React.useState([])
  const [riskSummary, setRiskSummary] = React.useState(null)

  React.useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch summary
      const summaryRes = await fetch('http://localhost:8000/api/analytics/dashboard-summary')
      const summaryData = await summaryRes.json()
      setSummary(summaryData.data)

      // Fetch risk summary
      const riskRes = await fetch('http://localhost:8000/api/inventory/summary')
      const riskData = await riskRes.json()
      setRiskSummary(riskData.data)

      // Mock sales trends
      const mockTrends = Array.from({ length: 30 }, (_, i) => ({
        day: i + 1,
        sales: Math.floor(Math.random() * 1000) + 500,
        revenue: Math.floor(Math.random() * 5000) + 2000
      }))
      setSalesTrends(mockTrends)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-8 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold mb-2">Retail Intelligence Dashboard</h1>
        <p className="text-blue-100">Real-time analytics & demand forecasting</p>
      </div>

      {/* KPI Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <KPICard
            title="Total Products"
            value={summary.total_products}
            icon={<Package className="w-8 h-8" />}
            color="blue"
          />
          <KPICard
            title="Inventory Value"
            value={`${Math.floor(summary.total_inventory)}` }
            icon={<Eye className="w-8 h-8" />}
            color="green"
          />
          <KPICard
            title="Recent Revenue"
            value={`$${Math.floor(summary.recent_sales_revenue)}`}
            icon={<TrendingUp className="w-8 h-8" />}
            color="purple"
          />
          {riskSummary && (
            <KPICard
              title="Critical Alerts"
              value={riskSummary.critical_alerts}
              icon={<AlertCircle className="w-8 h-8" />}
              color="red"
            />
          )}
        </div>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sales Trend Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Sales Trend (30 Days)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={salesTrends}>
              <defs>
                <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="sales" stroke="#3b82f6" fillOpacity={1} fill="url(#colorSales)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Revenue Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Revenue Trend (30 Days)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={salesTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" stroke="#10b981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Risk Overview */}
      {riskSummary && (
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle className="w-6 h-6 text-red-500" />
            <h2 className="text-lg font-semibold">Inventory Risk Overview</h2>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-red-50 p-4 rounded">
              <p className="text-sm text-gray-600">Critical Alerts</p>
              <p className="text-2xl font-bold text-red-600">{riskSummary.critical_alerts}</p>
            </div>
            <div className="bg-orange-50 p-4 rounded">
              <p className="text-sm text-gray-600">High Risk</p>
              <p className="text-2xl font-bold text-orange-600">{riskSummary.high_risk_products}</p>
            </div>
            <div className="bg-blue-50 p-4 rounded">
              <p className="text-sm text-gray-600">Total Monitored</p>
              <p className="text-2xl font-bold text-blue-600">{riskSummary.total_products}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

const KPICard = ({ title, value, icon, color }) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    purple: 'bg-purple-50 text-purple-600 border-purple-200',
    red: 'bg-red-50 text-red-600 border-red-200'
  }

  return (
    <div className={`${colorClasses[color]} p-6 rounded-lg border-2 shadow-sm hover:shadow-md transition`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className="opacity-20">{icon}</div>
      </div>
    </div>
  )
}

export default Dashboard
