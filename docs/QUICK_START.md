# Quick Reference Guide

## Starting the Platform

### Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Local Development
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

## Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Dashboard & UI |
| Backend | http://localhost:8000 | API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| PgAdmin | http://localhost:5050 | DB Admin |
| Database | localhost:5432 | PostgreSQL |

## Common Tasks

### Run Forecast
```bash
curl -X POST "http://localhost:8000/api/forecasting/forecast/SKU001?days=7"
```

### Check Inventory Risk
```bash
curl "http://localhost:8000/api/inventory/summary"
```

### Get Recommendations
```bash
curl "http://localhost:8000/api/inventory/recommendations"
```

### Query Assistant
```bash
curl -X POST "http://localhost:8000/api/assistant/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which products may stock out?"}'
```

## Database Credentials
- **User**: retail_user
- **Password**: retail_password
- **Database**: retail_db
- **Host**: localhost (or postgres in Docker)
- **Port**: 5432

## File Structure Cheat Sheet

```
backend/
├── app/
│   ├── api/          → FastAPI routes
│   ├── ml/           → ML models (forecasting, risk)
│   ├── models/       → SQLAlchemy DB models
│   ├── services/     → Business logic
│   ├── assistant/    → AI assistant
│   ├── utils/        → Database, helpers
│   └── main.py       → App entry point
└── requirements.txt  → Python dependencies

frontend/
├── src/
│   ├── pages/        → React pages
│   ├── App.jsx       → Main component
│   ├── main.jsx      → Entry point
│   └── index.css     → Styles
├── package.json      → Dependencies
└── vite.config.js    → Build config

database/
├── migrations/       → SQL schemas
└── seeds/           → Sample data

docker/
├── Dockerfile.backend
└── Dockerfile.frontend
```

## Troubleshooting Quick Fixes

| Issue | Command |
|-------|---------|
| Services won't start | `docker-compose down -v && docker-compose up -d` |
| API not responding | `curl http://localhost:8000/health` |
| DB connection failed | `psql -U retail_user -d retail_db` |
| Port in use | `netstat -ano \| findstr :8000` |
| Rebuild needed | `docker-compose build --no-cache` |

## Development Tips

1. **Hot Reload**: Enabled for both backend and frontend in dev mode
2. **API Testing**: Use http://localhost:8000/docs for Swagger UI
3. **Database**: Use PgAdmin at http://localhost:5050 for visualization
4. **Logs**: Check `docker-compose logs [service]` for debugging

## Sample Queries for Assistant

- "Which products may stock out next week?"
- "Show top declining products"
- "Forecast next month demand"
- "What are the top selling products?"
- "Show inventory trends"

## Key ML Models

### ARIMA (Autoregressive Integrated Moving Average)
- Captures temporal patterns
- Good for seasonal data
- Fast predictions

### Gradient Boosting (XGBoost)
- Learns non-linear relationships
- Handles multiple features
- More accurate but slower

### Hybrid Ensemble
- Combines both models (40% ARIMA + 60% GB)
- Best overall performance

## Risk Scoring Formula

```
Risk Score = 0-100
- z_score = inverse normal CDF(service_level)
- safety_stock = z_score × demand_std × sqrt(lead_time)
- reorder_point = (mean_demand × lead_time) + safety_stock
- risk = 100 × (1 - current_stock / reorder_point)
```

## Performance Benchmarks

- Forecast generation: ~500ms
- Risk analysis (1 product): ~100ms
- Risk analysis (all products): ~1s
- Assistant query: ~200ms

## Next Steps After Setup

1. ✅ Access dashboard at http://localhost:3000
2. ✅ Generate forecast for a product
3. ✅ View inventory risk analysis
4. ✅ Try AI assistant queries
5. ✅ Explore API documentation
6. ✅ Seed more sample data if needed

## Getting Help

- API Docs: http://localhost:8000/docs
- Setup Guide: `/docs/SETUP.md`
- API Examples: `/docs/API.md`
- Backend Logs: `docker-compose logs backend`

## Production Checklist

- [ ] Update .env with production values
- [ ] Set DEBUG=False
- [ ] Enable HTTPS
- [ ] Add authentication (JWT/API Key)
- [ ] Set up log aggregation
- [ ] Configure backups
- [ ] Set up monitoring/alerting
- [ ] Use production database
- [ ] Deploy with proper secrets management
