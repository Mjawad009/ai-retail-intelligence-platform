import React from 'react'
import { AlertCircle, AlertTriangle, AlertOctagon } from 'lucide-react'

const InventoryRisk = () => {
  const [risks, setRisks] = React.useState([])
  const [recommendations, setRecommendations] = React.useState(null)
  const [loading, setLoading] = React.useState(false)

  React.useEffect(() => {
    fetchRiskData()
  }, [])

  const fetchRiskData = async () => {
    setLoading(true)
    try {
      // Fetch all risks
      const riskRes = await fetch('http://localhost:8000/api/inventory/analyze-all')
      const riskData = await riskRes.json()
      
      if (riskData.status === 'success') {
        setRisks(riskData.data)
      }

      // Fetch recommendations
      const recRes = await fetch('http://localhost:8000/api/inventory/recommendations')
      const recData = await recRes.json()
      
      if (recData.status === 'success') {
        setRecommendations(recData.data)
      }
    } catch (error) {
      console.error('Error fetching risk data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (level) => {
    const colors = {
      'low': 'text-green-600 bg-green-50',
      'medium': 'text-yellow-600 bg-yellow-50',
      'high': 'text-orange-600 bg-orange-50',
      'critical': 'text-red-600 bg-red-50'
    }
    return colors[level] || colors.low
  }

  const getRiskIcon = (level) => {
    const icons = {
      'low': <AlertCircle className="w-5 h-5" />,
      'medium': <AlertCircle className="w-5 h-5" />,
      'high': <AlertTriangle className="w-5 h-5" />,
      'critical': <AlertOctagon className="w-5 h-5" />
    }
    return icons[level] || icons.low
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-red-600 to-red-800 text-white p-8 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <AlertTriangle />
          Inventory Risk Management
        </h1>
        <p className="text-red-100">Safety stock & stockout prevention</p>
      </div>

      {/* Risk Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <RiskMetric label="Critical" value={risks.filter(r => r.critical_alert).length} color="red" />
        <RiskMetric label="High Risk" value={risks.filter(r => r.stockout_risk_level === 'high').length} color="orange" />
        <RiskMetric label="Medium Risk" value={risks.filter(r => r.stockout_risk_level === 'medium').length} color="yellow" />
        <RiskMetric label="Low Risk" value={risks.filter(r => r.stockout_risk_level === 'low').length} color="green" />
      </div>

      {/* Reorder Recommendations */}
      {recommendations && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Reorder Recommendations</h2>
          <div className="space-y-4">
            {recommendations.immediate && recommendations.immediate.length > 0 && (
              <RecommendationSection
                title="Immediate Action Required"
                items={recommendations.immediate}
                color="red"
              />
            )}
            {recommendations.urgent && recommendations.urgent.length > 0 && (
              <RecommendationSection
                title="Urgent (1-2 Days)"
                items={recommendations.urgent}
                color="orange"
              />
            )}
            {recommendations.soon && recommendations.soon.length > 0 && (
              <RecommendationSection
                title="Soon (1 Week)"
                items={recommendations.soon}
                color="yellow"
              />
            )}
          </div>
        </div>
      )}

      {/* Risk Details Table */}
      <div className="bg-white p-6 rounded-lg shadow overflow-x-auto">
        <h2 className="text-lg font-semibold mb-4">Product Risk Analysis</h2>
        <table className="w-full text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left">Product ID</th>
              <th className="px-4 py-2 text-left">Current Stock</th>
              <th className="px-4 py-2 text-left">Reorder Point</th>
              <th className="px-4 py-2 text-left">Safety Stock</th>
              <th className="px-4 py-2 text-left">Risk Score</th>
              <th className="px-4 py-2 text-left">Days to Stockout</th>
              <th className="px-4 py-2 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            {risks.map((risk, idx) => (
              <tr key={idx} className="border-b hover:bg-gray-50">
                <td className="px-4 py-2 font-medium">{risk.product_id}</td>
                <td className="px-4 py-2">{risk.current_stock.toFixed(0)}</td>
                <td className="px-4 py-2">{risk.reorder_point.toFixed(0)}</td>
                <td className="px-4 py-2">{risk.safety_stock.toFixed(0)}</td>
                <td className="px-4 py-2">
                  <span className={`px-3 py-1 rounded text-xs font-semibold ${getRiskColor(risk.stockout_risk_level)}`}>
                    {risk.stockout_risk_score.toFixed(1)}
                  </span>
                </td>
                <td className="px-4 py-2">{risk.days_to_potential_stockout.toFixed(1)}</td>
                <td className="px-4 py-2">
                  <div className={`flex items-center gap-1 ${getRiskColor(risk.stockout_risk_level)}`}>
                    {getRiskIcon(risk.stockout_risk_level)}
                    <span className="capitalize">{risk.stockout_risk_level}</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

const RiskMetric = ({ label, value, color }) => {
  const colorClasses = {
    red: 'bg-red-50 text-red-600 border-red-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200',
    yellow: 'bg-yellow-50 text-yellow-600 border-yellow-200',
    green: 'bg-green-50 text-green-600 border-green-200'
  }

  return (
    <div className={`${colorClasses[color]} border-2 p-4 rounded-lg text-center`}>
      <p className="text-sm font-medium text-gray-600">{label}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  )
}

const RecommendationSection = ({ title, items, color }) => {
  const colorClasses = {
    red: 'border-red-200 bg-red-50',
    orange: 'border-orange-200 bg-orange-50',
    yellow: 'border-yellow-200 bg-yellow-50'
  }

  return (
    <div className={`${colorClasses[color]} border-2 p-4 rounded-lg`}>
      <h3 className="font-semibold mb-3">{title}</h3>
      <div className="space-y-2">
        {items.map((item, idx) => (
          <div key={idx} className="bg-white p-3 rounded flex justify-between items-center">
            <div>
              <p className="font-medium">{item.product_id}</p>
              <p className="text-xs text-gray-600">{item.reason}</p>
            </div>
            <div className="text-right">
              <p className="font-bold text-lg">{item.suggested_quantity.toFixed(0)}</p>
              <p className="text-xs text-gray-600">units</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default InventoryRisk
