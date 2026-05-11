"""Forecasting API Endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.forecasting_service import ForecastingService
from app.utils.database import get_db

router = APIRouter(prefix="/api/forecasting", tags=["Forecasting"])


class ForecastRequest:
    def __init__(self, product_id: str, days: int = 7):
        self.product_id = product_id
        self.days = days


class MultiProductForecastRequest:
    def __init__(self, product_ids: List[str], days: int = 7):
        self.product_ids = product_ids
        self.days = days


@router.post("/forecast/{product_id}")
async def forecast_product(
    product_id: str,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Forecast demand for a single product"""
    service = ForecastingService(db)
    forecast = service.forecast_product_demand(product_id, days)
    
    if not forecast:
        raise HTTPException(status_code=404, detail="Could not generate forecast")
    
    return {
        "status": "success",
        "data": forecast
    }


@router.post("/forecast-multiple")
async def forecast_multiple(
    request: dict,
    db: Session = Depends(get_db)
):
    """Forecast for multiple products"""
    product_ids = request.get('product_ids', [])
    days = request.get('days', 7)
    
    if not product_ids:
        raise HTTPException(status_code=400, detail="product_ids required")
    
    service = ForecastingService(db)
    forecasts = service.forecast_multiple_products(product_ids, days)
    
    return {
        "status": "success",
        "count": len(forecasts),
        "data": forecasts
    }


@router.get("/evaluate/{product_id}")
async def evaluate_forecast(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Evaluate forecast accuracy for a product"""
    service = ForecastingService(db)
    evaluation = service.evaluate_forecast(product_id)
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="No forecast found for evaluation")
    
    return {
        "status": "success",
        "data": evaluation
    }


@router.get("/history/{product_id}")
async def get_forecast_history(
    product_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get forecast history for a product"""
    service = ForecastingService(db)
    history = service.get_forecast_history(product_id, limit)
    
    return {
        "status": "success",
        "count": len(history),
        "data": history
    }
