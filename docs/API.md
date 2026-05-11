# API Examples & Usage Guide

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required. In production, add JWT tokens or API keys.

---

## Forecasting Endpoints

### 1. Generate Single Product Forecast

**Endpoint**: `POST /api/forecasting/forecast/{product_id}`

**Parameters**:
- `product_id` (path): Product identifier (e.g., "SKU001")
- `days` (query): Forecast days (default: 7, max: 30)

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/forecasting/forecast/SKU001?days=14"
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "product_id": "SKU001",
    "forecast_date": "2024-01-15T10:30:00",
    "days": 14,
    "hybrid_forecast": [25.5, 26.2, 24.8, ...],
    "arima_forecast": [24.1, 26.5, 23.9, ...],
    "gradient_boosting": [27.2, 25.8, 25.5, ...]
  }
}
```

---

### 2. Forecast Multiple Products

**Endpoint**: `POST /api/forecasting/forecast-multiple`

**Request Body**:
```json
{
  "product_ids": ["SKU001", "SKU002", "SKU003"],
  "days": 7
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/forecasting/forecast-multiple" \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": ["SKU001", "SKU002"],
    "days": 10
  }'
```

**Response**:
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "product_id": "SKU001",
      "hybrid_forecast": [25.5, 26.2, ...],
      ...
    },
    {
      "product_id": "SKU002",
      "hybrid_forecast": [12.1, 13.5, ...],
      ...
    }
  ]
}
```

---

### 3. Evaluate Forecast Accuracy

**Endpoint**: `GET /api/forecasting/evaluate/{product_id}`

**Example Request**:
```bash
curl "http://localhost:8000/api/forecasting/evaluate/SKU001"
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "product_id": "SKU001",
    "forecast_date": "2024-01-15T10:30:00",
    "forecast_days": 7,
    "actual_sales": [23, 25, 24, 26, 25, 24, 23],
    "forecast": [25.5, 26.2, 24.8, 25.1, 24.9, 25.3, 24.7],
    "metrics": {
      "mae": 1.2,
      "rmse": 1.5,
      "mape": 5.3
    }
  }
}
```

---

### 4. Get Forecast History

**Endpoint**: `GET /api/forecasting/history/{product_id}`

**Parameters**:
- `limit` (query): Number of records (default: 10)

**Example Request**:
```bash
curl "http://localhost:8000/api/forecasting/history/SKU001?limit=5"
```

**Response**:
```json
{
  "status": "success",
  "count": 5,
  "data": [
    {
      "forecast_date": "2024-01-15T10:30:00",
      "forecast_days": 7,
      "hybrid_forecast": [25.5, 26.2, ...],
      "arima_forecast": [24.1, 26.5, ...],
      "gb_forecast": [27.2, 25.8, ...]
    },
    ...
  ]
}
```

---

## Inventory Risk Endpoints

### 1. Analyze Single Product Risk

**Endpoint**: `POST /api/inventory/analyze/{product_id}`

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/inventory/analyze/SKU001"
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "product_id": "SKU001",
    "current_stock": 45,
    "daily_demand_mean": 15.5,
    "daily_demand_std": 3.2,
    "safety_stock": 12.3,
    "reorder_point": 120.8,
    "stockout_risk_score": 35.2,
    "stockout_risk_level": "medium",
    "recommended_order_qty": 150,
    "economic_order_qty": 142.5,
    "days_to_potential_stockout": 2.9,
    "reorder_recommended": true,
    "critical_alert": false
  }
}
```

---

### 2. Analyze All Products

**Endpoint**: `POST /api/inventory/analyze-all`

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/inventory/analyze-all"
```

**Response**:
```json
{
  "status": "success",
  "count": 8,
  "data": [
    { "product_id": "SKU001", ... },
    { "product_id": "SKU002", ... },
    ...
  ]
}
```

---

### 3. Get Risk Summary

**Endpoint**: `GET /api/inventory/summary`

**Example Request**:
```bash
curl "http://localhost:8000/api/inventory/summary"
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_products": 8,
    "critical_alerts": 2,
    "high_risk_products": 3,
    "critical_products": ["SKU001", "SKU004"],
    "high_risk_products_list": ["SKU002", "SKU003", "SKU005"]
  }
}
```

---

### 4. Generate Reorder Recommendations

**Endpoint**: `POST /api/inventory/recommendations`

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/inventory/recommendations"
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "immediate": [
      {
        "product_id": "SKU001",
        "reason": "Critical stockout risk",
        "suggested_quantity": 150,
        "priority": 1
      }
    ],
    "urgent": [
      {
        "product_id": "SKU002",
        "reason": "Stockout in ~2.5 days",
        "suggested_quantity": 120,
        "priority": 2
      }
    ],
    "soon": [...],
    "optimal": [...],
    "no_action": [...]
  }
}
```

---

### 5. Get Pending Recommendations

**Endpoint**: `GET /api/inventory/recommendations`

**Parameters**:
- `category` (query, optional): "immediate", "urgent", "soon", "optimal"

**Example Request**:
```bash
curl "http://localhost:8000/api/inventory/recommendations?category=urgent"
```

**Response**:
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": 1,
      "product_id": "SKU002",
      "category": "urgent",
      "reason": "Stockout in ~2.5 days",
      "suggested_quantity": 120,
      "priority": 2,
      "recommendation_date": "2024-01-15T10:30:00"
    },
    ...
  ]
}
```

---

## Analytics Endpoints

### 1. Get Sales Trends

**Endpoint**: `GET /api/analytics/sales-trends`

**Parameters**:
- `product_id` (query): Product identifier
- `days` (query): Number of days (default: 30)

**Example Request**:
```bash
curl "http://localhost:8000/api/analytics/sales-trends?product_id=SKU001&days=30"
```

**Response**:
```json
{
  "status": "success",
  "product_id": "SKU001",
  "data": {
    "dates": ["2024-01-01", "2024-01-02", ...],
    "sales": [25, 28, 24, 26, ...],
    "average": 25.5,
    "trend": "up"
  }
}
```

---

### 2. Get Inventory Trends

**Endpoint**: `GET /api/analytics/inventory-trends`

**Parameters**:
- `product_id` (query, optional): Specific product or all

**Example Request (Single Product)**:
```bash
curl "http://localhost:8000/api/analytics/inventory-trends?product_id=SKU001"
```

**Response**:
```json
{
  "status": "success",
  "product_id": "SKU001",
  "data": {
    "current_stock": 45,
    "reserved_stock": 5,
    "available_stock": 40,
    "last_update": "2024-01-15T10:30:00"
  }
}
```

**Example Request (All Products)**:
```bash
curl "http://localhost:8000/api/analytics/inventory-trends"
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_inventory_value": 1250,
    "products_low_stock": 3,
    "total_products": 8
  }
}
```

---

### 3. Get Product Performance

**Endpoint**: `GET /api/analytics/product-performance`

**Parameters**:
- `days` (query): Period (default: 30)

**Example Request**:
```bash
curl "http://localhost:8000/api/analytics/product-performance?days=30"
```

**Response**:
```json
{
  "status": "success",
  "count": 8,
  "data": [
    {
      "product_id": "SKU001",
      "product_name": "Laptop",
      "total_sales": 120,
      "total_revenue": 60000,
      "current_stock": 45,
      "avg_daily_sales": 4.0
    },
    ...
  ]
}
```

---

### 4. Get Dashboard Summary

**Endpoint**: `GET /api/analytics/dashboard-summary`

**Example Request**:
```bash
curl "http://localhost:8000/api/analytics/dashboard-summary"
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_products": 8,
    "total_inventory": 1250,
    "recent_sales_quantity": 450,
    "recent_sales_revenue": 18500,
    "low_stock_alerts": 3
  }
}
```

---

## AI Assistant Endpoints

### 1. Process Natural Language Query

**Endpoint**: `POST /api/assistant/query`

**Request Body**:
```json
{
  "query": "Which products may stock out next week?"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/assistant/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which products may stock out next week?"}'
```

**Response**:
```json
{
  "status": "success",
  "query": "Which products may stock out next week?",
  "response": {
    "query_type": "stockout_risk",
    "answer": "Found 2 products with critical stockout risk:",
    "products": [
      {
        "product_id": "SKU001",
        "risk_score": 75.3,
        "days_to_stockout": 2.5,
        "current_stock": 45,
        "recommended_order": 150
      },
      {
        "product_id": "SKU002",
        "risk_score": 68.2,
        "days_to_stockout": 3.1,
        "current_stock": 120,
        "recommended_order": 120
      }
    ]
  }
}
```

---

### 2. Get Query Suggestions

**Endpoint**: `GET /api/assistant/suggestions`

**Example Request**:
```bash
curl "http://localhost:8000/api/assistant/suggestions"
```

**Response**:
```json
{
  "status": "success",
  "suggestions": [
    "Which products may stock out next week?",
    "Show top declining products",
    "Forecast next month demand",
    "What are the top selling products?",
    "Show me products with low inventory",
    "Which products have highest revenue?",
    "Show sales trends for the last 30 days",
    "What inventory level should we maintain?"
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "product_ids required"
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Product not found"
}
```

### 500 Server Error
```json
{
  "status": "error",
  "message": "Internal server error"
}
```

---

## Using with Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Forecast
response = requests.post(
    f"{BASE_URL}/api/forecasting/forecast/SKU001",
    params={"days": 14}
)
forecast = response.json()

# Analyze Risk
response = requests.post(
    f"{BASE_URL}/api/inventory/analyze/SKU001"
)
risk = response.json()

# Query Assistant
response = requests.post(
    f"{BASE_URL}/api/assistant/query",
    json={"query": "Which products may stock out?"}
)
answer = response.json()
```

---

## Using with JavaScript/Fetch

```javascript
const BASE_URL = 'http://localhost:8000'

// Forecast
const forecast = await fetch(
  `${BASE_URL}/api/forecasting/forecast/SKU001?days=14`,
  { method: 'POST' }
).then(r => r.json())

// Query Assistant
const response = await fetch(
  `${BASE_URL}/api/assistant/query`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: 'Which products may stock out?' })
  }
).then(r => r.json())
```

---

## Rate Limiting & Quotas

Currently no rate limiting. For production:
- Implement request throttling
- Add IP-based rate limits
- Add user-based quotas

---

## Webhook Support (Future)

Planned features:
- Inventory alerts webhook
- Reorder notifications webhook
- Forecast updates webhook
