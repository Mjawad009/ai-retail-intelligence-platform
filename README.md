# AI Retail Intelligence & Autonomous Demand Optimization Platform

A comprehensive end-to-end retail analytics system combining time-series forecasting, inventory risk modeling, and AI-powered insights.

<img width="1869" height="872" alt="Screenshot_11-5-2026_125640_localhost" src="https://github.com/user-attachments/assets/4e9728b7-f468-4837-8649-7dc8423125fe" />


## Features

### 1. **Demand Forecasting**
- ARIMA time-series forecasting
- Gradient Boosting machine learning model
- Hybrid ensemble predictions
- Multi-product forecasting support
- Accuracy metrics: MAE, RMSE, MAPE

### 2. **Inventory Risk Modeling**
- Safety stock calculation
- Reorder point determination
- Stockout risk scoring (0-100)
- Automated reorder recommendations
- Economic Order Quantity (EOQ) optimization

### 3. **Analytics Dashboard**
- Real-time sales trends
- Inventory trends and KPIs
- Forecast visualization
- Risk alerts and notifications
- Product performance metrics

### 4. **AI Analytics Assistant**
- Natural language queries
- Questions like:
  - "Which products may stock out next week?"
  - "Show top declining products"
  - "Forecast next month demand"
- Intelligent query classification

### 5. **FastAPI Microservices**
- RESTful API endpoints
- Forecasting service
- Inventory risk analysis
- Analytics queries
- Assistant interface

### 6. **Docker Support**
- Complete containerization
- Docker Compose orchestration
- PostgreSQL database
- PgAdmin management

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **ML Libraries**: 
  - ARIMA: statsmodels
  - Gradient Boosting: XGBoost, scikit-learn
  - Data Processing: Pandas, NumPy
- **Database**: PostgreSQL

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Charting**: Recharts
- **Build Tool**: Vite

### Deployment
- **Containerization**: Docker
- **Orchestration**: Docker Compose

## Project Structure

```
ai-retail-project/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI routes
│   │   ├── ml/            # ML models
│   │   ├── models/        # Database models
│   │   ├── services/      # Business logic
│   │   ├── assistant/     # AI assistant
│   │   ├── utils/         # Utilities
│   │   └── main.py        # Main app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/         # React pages
│   │   ├── components/    # React components
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
├── database/
│   ├── migrations/        # SQL migrations
│   └── seeds/             # Sample data
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
├── .env
└── README.md
```

## Prerequisites

- Docker & Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 15+

## Quick Start with Docker Compose

### 1. Clone/Setup Project
```bash
cd ai-retail-project
```

### 2. Start Services
```bash
docker-compose up -d
```

### 3. Initialize Database
```bash
docker-compose exec postgres psql -U retail_user -d retail_db -f /docker-entrypoint-initdb.d/001_initial_schema.sql
```

### 4. Seed Sample Data
```bash
docker-compose exec postgres psql -U retail_user -d retail_db -f /docker-entrypoint-initdb.d/../../../database/seeds/sample_data.sql
```

### 5. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | - |
| Backend API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| PgAdmin | http://localhost:5050 | admin@example.com / admin |
| Database | localhost:5432 | retail_user / retail_password |

## Manual Setup (Without Docker)

### Backend Setup

#### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 2. Set Environment Variables
```bash
# Linux/Mac
export DATABASE_URL=postgresql://retail_user:retail_password@localhost:5432/retail_db

# Windows
set DATABASE_URL=postgresql://retail_user:retail_password@localhost:5432/retail_db
```

#### 3. Initialize Database
```bash
# Create database manually or use:
psql -U postgres -c "CREATE USER retail_user WITH PASSWORD 'retail_password';"
psql -U postgres -c "CREATE DATABASE retail_db OWNER retail_user;"
psql -U retail_user -d retail_db -f ../database/migrations/001_initial_schema.sql
psql -U retail_user -d retail_db -f ../database/seeds/sample_data.sql
```

#### 4. Run Backend
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

#### 1. Install Dependencies
```bash
cd frontend
npm install
```

#### 2. Run Development Server
```bash
npm run dev
```

The frontend will open at `http://localhost:3000`

## API Endpoints

### Forecasting
- `POST /api/forecasting/forecast/{product_id}` - Generate forecast
- `POST /api/forecasting/forecast-multiple` - Forecast multiple products
- `GET /api/forecasting/evaluate/{product_id}` - Evaluate accuracy
- `GET /api/forecasting/history/{product_id}` - Get history

### Inventory
- `POST /api/inventory/analyze/{product_id}` - Analyze risk
- `POST /api/inventory/analyze-all` - Analyze all products
- `GET /api/inventory/summary` - Risk summary
- `POST /api/inventory/recommendations` - Generate recommendations
- `GET /api/inventory/recommendations?category=urgent` - Get recommendations

### Analytics
- `GET /api/analytics/sales-trends?product_id=SKU001&days=30` - Sales trends
- `GET /api/analytics/inventory-trends` - Inventory trends
- `GET /api/analytics/product-performance` - Product performance
- `GET /api/analytics/dashboard-summary` - Dashboard summary

### Assistant
- `POST /api/assistant/query` - Process query
- `GET /api/assistant/suggestions` - Get suggestions

## Example Queries (AI Assistant)

```
"Which products may stock out next week?"
"Show top declining products"
"Forecast next month demand"
"What are the top selling products?"
"Show me products with low inventory"
"Which products have highest revenue?"
"Show sales trends for the last 30 days"
"What inventory level should we maintain?"
```

## Configuration

### .env File
```env
DATABASE_URL=postgresql://retail_user:retail_password@localhost:5432/retail_db
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

### Database Connection
Update `DATABASE_URL` in `.env` if using different credentials

## Features Explained

### Demand Forecasting
- **ARIMA**: Captures temporal patterns and seasonality
- **Gradient Boosting**: Learns complex non-linear relationships
- **Hybrid**: Weighted ensemble combines both approaches
- Output: 7-30 day demand predictions with accuracy metrics

### Inventory Risk Scoring
```
Risk Score = 0-100
- 0-20:   Low Risk (adequate stock)
- 20-50:  Medium Risk (monitor)
- 50-70:  High Risk (consider reordering)
- 70-100: Critical (reorder immediately)
```

### Reorder Recommendations
- **Immediate**: Critical stockout risk
- **Urgent**: Stockout within 1-2 days
- **Soon**: Reorder point approaching
- **Optimal**: Based on Economic Order Quantity

## Performance Considerations

- **Database**: Indexed on product_id, dates, and status for fast queries
- **API**: Connection pooling with max 10 connections
- **ML**: Incremental model updates, caching of forecasts
- **Frontend**: Lazy loading, responsive charts

## Troubleshooting

### Database Connection Issues
```bash
# Test connection
psql -U retail_user -d retail_db -h localhost

# Check logs
docker-compose logs postgres
```

### Backend Errors
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Frontend Issues
```bash
# Clear cache and reinstall
rm -rf frontend/node_modules frontend/package-lock.json
cd frontend && npm install
npm run dev
```

## Development Workflow

### Adding New Features
1. Create feature branch
2. Update backend services in `backend/app/services/`
3. Create/update API endpoints in `backend/app/api/`
4. Update frontend pages in `frontend/src/pages/`
5. Test via API docs: http://localhost:8000/docs

### Database Migrations
1. Create SQL migration in `database/migrations/`
2. Update SQLAlchemy models in `backend/app/models/models.py`
3. Apply migration:
```bash
docker-compose exec postgres psql -U retail_user -d retail_db -f /migration.sql
```

## Production Deployment

### Using Docker Compose
```bash
# Build images
docker-compose build

# Deploy
docker-compose up -d

# View logs
docker-compose logs -f
```

### Environment Variables for Production
```env
DATABASE_URL=postgresql://user:password@prod-db:5432/retail_db
DEBUG=False
LOG_LEVEL=WARNING
PYTHONUNBUFFERED=1
```

## Monitoring & Maintenance

### View Logs
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

### Database Backup
```bash
docker-compose exec postgres pg_dump -U retail_user retail_db > backup.sql
```

### Database Restore
```bash
docker-compose exec postgres psql -U retail_user retail_db < backup.sql
```

## Performance Metrics

The system tracks:
- **Forecast Accuracy**: MAE, RMSE, MAPE
- **Inventory Health**: Safety stock coverage, reorder frequency
- **Risk Metrics**: Stockout probability, safety index
- **Business Metrics**: Revenue, inventory turnover

## Future Enhancements

- [ ] Real-time data streaming (Kafka)
- [ ] Advanced ML models (Prophet, LSTM)
- [ ] Multi-location inventory optimization
- [ ] Supplier integration
- [ ] Automated ordering system
- [ ] Mobile app
- [ ] Advanced analytics (anomaly detection)

## Support & Documentation

- API Documentation: http://localhost:8000/docs
- Database Schema: `database/migrations/001_initial_schema.sql`
- Sample Data: `database/seeds/sample_data.sql`

## License

MIT License

## Contributors

Built with attention to retail analytics best practices and modern ML/AI techniques.
