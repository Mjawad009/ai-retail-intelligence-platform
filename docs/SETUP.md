# AI Retail Intelligence Platform - Setup Guide

## System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space
- **Docker**: 20.10+ (for Docker setup)
- **Node.js**: 18+ (for local frontend development)
- **Python**: 3.11+ (for local backend development)
- **PostgreSQL**: 15+ (for local database)

## Option 1: Docker Compose Setup (Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Git

### Step-by-Step Setup

#### 1. Clone or Extract Project
```bash
cd "C:\Users\Jawad Hassan\Documents\Custom Office Templates\ai retail project"
```

#### 2. Configure Environment
Create `.env` file with contents:
```env
DATABASE_URL=postgresql://retail_user:retail_password@postgres:5432/retail_db
PYTHONUNBUFFERED=1
REACT_APP_API_URL=http://localhost:8000
```

#### 3. Start All Services
```bash
docker-compose up -d
```

Wait 30 seconds for services to start. Monitor logs:
```bash
docker-compose logs -f
```

#### 4. Initialize Database (First Time Only)
```bash
# In PowerShell
docker-compose exec postgres psql -U retail_user -d retail_db -f /docker-entrypoint-initdb.d/001_initial_schema.sql
```

#### 5. Access Applications

| Application | URL | Purpose |
|------------|-----|---------|
| Dashboard | http://localhost:3000 | Main UI |
| API Docs | http://localhost:8000/docs | API documentation |
| PgAdmin | http://localhost:5050 | Database management |

#### 6. Test Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "..."}
```

### Managing Docker Services

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart backend
docker-compose restart frontend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild images
docker-compose build --no-cache
```

---

## Option 2: Local Development Setup

### Prerequisites
- PostgreSQL installed and running
- Python 3.11+
- Node.js 18+

### Backend Setup

#### 1. Install Python Dependencies
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### 2. Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Execute these commands:
CREATE USER retail_user WITH PASSWORD 'retail_password';
CREATE DATABASE retail_db OWNER retail_user;
\q
```

#### 3. Initialize Schema
```bash
psql -U retail_user -d retail_db -f ..\database\migrations\001_initial_schema.sql
```

#### 4. Seed Sample Data
```bash
psql -U retail_user -d retail_db -f ..\database\seeds\sample_data.sql
```

#### 5. Set Environment Variables
```powershell
# PowerShell
$env:DATABASE_URL = "postgresql://retail_user:retail_password@localhost:5432/retail_db"

# Command Prompt
set DATABASE_URL=postgresql://retail_user:retail_password@localhost:5432/retail_db

# Linux/macOS
export DATABASE_URL=postgresql://retail_user:retail_password@localhost:5432/retail_db
```

#### 6. Run Backend
```bash
python -m uvicorn app.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000

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

Frontend will automatically open at: http://localhost:3000

---

## First Time Testing

### 1. Create Sample Product
```bash
curl -X POST http://localhost:8000/api/forecasting/forecast/SKU001?days=7
```

### 2. Check Dashboard Summary
```bash
curl http://localhost:8000/api/analytics/dashboard-summary
```

### 3. Test AI Assistant
```bash
curl -X POST http://localhost:8000/api/assistant/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Which products may stock out?"}'
```

---

## Common Issues & Solutions

### Issue: Database Connection Failed
**Solution**:
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Verify credentials
psql -U retail_user -d retail_db

# Check env variable
echo %DATABASE_URL%  # Windows
echo $DATABASE_URL  # Linux/macOS
```

### Issue: Port Already in Use
**Solution**:
```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # macOS/Linux

# Kill process or change port in docker-compose.yml
```

### Issue: Docker Services Won't Start
**Solution**:
```bash
# Check Docker daemon
docker ps

# Restart Docker Desktop and try again
docker-compose down -v
docker-compose up -d
```

### Issue: Frontend API Connection Failed
**Solution**:
1. Verify backend is running: http://localhost:8000/health
2. Check browser console for CORS errors
3. Verify API_URL in docker-compose.yml or .env
4. Restart frontend: `docker-compose restart frontend`

### Issue: Database Migrations Failed
**Solution**:
```bash
# Reset database
docker-compose exec postgres dropdb -U retail_user retail_db
docker-compose exec postgres createdb -U retail_user retail_db

# Re-run migrations
docker-compose exec postgres psql -U retail_user -d retail_db -f /migration.sql
```

---

## Verification Checklist

- [ ] Docker services running: `docker-compose ps`
- [ ] Backend health check: `curl http://localhost:8000/health`
- [ ] Database connection works: `psql -U retail_user -d retail_db`
- [ ] Frontend loads: http://localhost:3000
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] Sample data present: `SELECT COUNT(*) FROM products;`

---

## Next Steps

1. **Explore Dashboard**: Navigate through different pages
2. **Run Forecast**: Generate demand forecast for a product
3. **Check Risks**: View inventory risk analysis
4. **Try Assistant**: Ask natural language questions
5. **Review API Docs**: Visit http://localhost:8000/docs

---

## Useful Commands

### Backend Logs
```bash
docker-compose logs -f backend --tail=50
```

### Database Query
```bash
docker-compose exec postgres psql -U retail_user -d retail_db
```

### Clear Database
```bash
docker-compose exec postgres psql -U retail_user -d retail_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

### Rebuild without Cache
```bash
docker-compose build --no-cache && docker-compose up -d
```

---

## Support

For issues or questions:
1. Check logs: `docker-compose logs [service]`
2. Review README.md
3. Check API docs: http://localhost:8000/docs
4. Verify environment variables in .env

Happy analyzing! 📊
