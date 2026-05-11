import React from 'react'
import { Send, Lightbulb } from 'lucide-react'

const Assistant = () => {
  const [query, setQuery] = React.useState('')
  const [messages, setMessages] = React.useState([
    {
      type: 'assistant',
      content: 'Hello! I\'m your Retail Analytics Assistant. Ask me about products, sales, inventory, or demand forecasts.'
    }
  ])
  const [suggestions, setSuggestions] = React.useState([])
  const [loading, setLoading] = React.useState(false)

  React.useEffect(() => {
    fetchSuggestions()
  }, [])

  const fetchSuggestions = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/assistant/suggestions')
      const data = await res.json()
      if (data.status === 'success') {
        setSuggestions(data.suggestions)
      }
    } catch (error) {
      console.error('Error fetching suggestions:', error)
    }
  }

  const handleSendQuery = async () => {
    if (!query.trim()) return

    // Add user message
    setMessages([...messages, { type: 'user', content: query }])
    setQuery('')
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8000/api/assistant/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })

      const data = await res.json()

      if (data.status === 'success') {
        const response = data.response
        let responseContent = response.answer

        if (response.products && response.products.length > 0) {
          responseContent += '\n\n' + formatProductsList(response.products)
        }

        setMessages(prev => [...prev, { type: 'assistant', content: responseContent }])
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { type: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion)
  }

  const formatProductsList = (products) => {
    if (!products || products.length === 0) return ''

    return products.map((p, i) => {
      let text = `${i + 1}. ${p.product_id}`
      if (p.product_name) text += ` - ${p.product_name}`
      if (p.current_stock !== undefined) text += ` (Stock: ${p.current_stock})`
      if (p.risk_score !== undefined) text += ` (Risk: ${p.risk_score.toFixed(1)})`
      if (p.total_revenue !== undefined) text += ` (Revenue: $${p.total_revenue.toFixed(0)})`
      if (p.decline_percentage !== undefined) text += ` (Decline: ${p.decline_percentage.toFixed(1)}%)`
      return text
    }).join('\n')
  }

  return (
    <div className="h-full flex flex-col space-y-4">
      <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white p-8 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Lightbulb />
          Analytics Assistant
        </h1>
        <p className="text-purple-100">Ask me questions about your retail data</p>
      </div>

      <div className="flex-1 flex flex-col space-y-4 bg-white rounded-lg shadow p-6 overflow-hidden">
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          {messages.map((msg, idx) => (
            <Message key={idx} message={msg} />
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg rounded-tl-none">
                <div className="flex gap-2">
                  <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Suggestions */}
        {messages.length === 1 && suggestions.length > 0 && (
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">Example queries:</p>
            <div className="grid grid-cols-1 gap-2">
              {suggestions.slice(0, 4).map((suggestion, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="text-left px-4 py-2 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 text-sm border border-purple-200"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendQuery()}
            placeholder="Ask about your retail data..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            disabled={loading}
          />
          <button
            onClick={handleSendQuery}
            disabled={!query.trim() || loading}
            className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
            Send
          </button>
        </div>
      </div>
    </div>
  )
}

const Message = ({ message }) => {
  const isUser = message.type === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        isUser
          ? 'bg-purple-600 text-white rounded-tr-none'
          : 'bg-gray-200 text-gray-800 rounded-tl-none'
      }`}>
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  )
}

export default Assistant
