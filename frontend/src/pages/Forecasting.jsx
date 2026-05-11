import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, AlertCircle } from 'lucide-react'

const Forecasting = () => {
  const [products, setProducts] = React.useState([])
  const [selectedProduct, setSelectedProduct] = React.useState('')
  const [forecast, setForecast] = React.useState(null)
  const [loading, setLoading] = React.useState(false)

  React.useEffect(() => {
    // Mock products
    setProducts([
      { id: 'SKU001', name: 'Laptop' },
      { id: 'SKU002', name: 'Mouse' },
      { id: 'SKU003', name: 'Keyboard' },
      { id: 'SKU004', name: 'Monitor' },
      { id: 'SKU005', name: 'Headphones' }
    ])
  }, [])

  const handleForecast = async () => {
    if (!selectedProduct) return

    setLoading(true)
    try {
      const res = await fetch(`http://localhost:8000/api/forecasting/forecast/${selectedProduct}?days=30`)
      const data = await res.json()
      
      if (data.status === 'success') {
        const forecastData = data.data
        
        // Create chart data
        const chartData = Array.from({ length: forecastData.hybrid_forecast.length }, (_, i) => ({
          day: i + 1,
          hybrid: forecastData.hybrid_forecast[i],
          arima: forecastData.arima_forecast[i],
          gradient_boosting: forecastData.gradient_boosting[i]
        }))
        
        setForecast(chartData)
      }
    } catch (error) {
      console.error('Error fetching forecast:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-green-600 to-green-800 text-white p-8 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <TrendingUp />
          Demand Forecasting
        </h1>
        <p className="text-green-100">Hybrid ARIMA + Gradient Boosting predictions</p>
      </div>

      {/* Product Selection */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-4">Select Product</h2>
        <div className="flex gap-4">
          <select
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value="">Choose a product...</option>
            {products.map(p => (
              <option key={p.id} value={p.id}>{p.name} ({p.id})</option>
            ))}
          </select>
          <button
            onClick={handleForecast}
            disabled={!selectedProduct || loading}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? 'Forecasting...' : 'Generate Forecast'}
          </button>
        </div>
      </div>

      {/* Forecast Chart */}
      {forecast && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">30-Day Demand Forecast</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={forecast}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" label={{ value: 'Day', position: 'insideBottomRight', offset: -5 }} />
              <YAxis label={{ value: 'Quantity', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="hybrid" stroke="#10b981" strokeWidth={2} name="Hybrid Forecast" />
              <Line type="monotone" dataKey="arima" stroke="#3b82f6" strokeWidth={1} name="ARIMA" strokeDasharray="5 5" />
              <Line type="monotone" dataKey="gradient_boosting" stroke="#f59e0b" strokeWidth={1} name="Gradient Boosting" strokeDasharray="5 5" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Forecast Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <InsightCard
          title="Model: Hybrid"
          description="ARIMA + Gradient Boosting ensemble"
          value="Recommended"
          color="green"
        />
        <InsightCard
          title="Forecast Horizon"
          description="Short-term demand prediction"
          value="7-30 days"
          color="blue"
        />
        <InsightCard
          title="Accuracy Metrics"
          description="MAE, RMSE, MAPE evaluated"
          value="See Details"
          color="purple"
        />
      </div>
    </div>
  )
}

const InsightCard = ({ title, description, value, color }) => {
  const colorClasses = {
    blue: 'border-blue-200 bg-blue-50',
    green: 'border-green-200 bg-green-50',
    purple: 'border-purple-200 bg-purple-50'
  }

  return (
    <div className={`${colorClasses[color]} border-2 p-4 rounded-lg`}>
      <p className="text-sm font-medium text-gray-600">{title}</p>
      <p className="text-xs text-gray-500 mt-1">{description}</p>
      <p className="text-lg font-bold mt-3">{value}</p>
    </div>
  )
}

export default Forecasting
