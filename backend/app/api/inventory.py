"""Inventory Risk API Endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.services.inventory_service import InventoryRiskService
from app.utils.database import get_db

router = APIRouter(prefix="/api/inventory", tags=["Inventory Risk"])


@router.post("/analyze/{product_id}")
async def analyze_product_risk(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Analyze inventory risk for a product"""
    service = InventoryRiskService(db)
    analysis = service.analyze_product_risk(product_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "status": "success",
        "data": analysis
    }


@router.post("/analyze-all")
async def analyze_all_risks(db: Session = Depends(get_db)):
    """Analyze inventory risk for all products"""
    service = InventoryRiskService(db)
    analyses = service.analyze_all_products()
    
    return {
        "status": "success",
        "count": len(analyses),
        "data": analyses
    }


@router.get("/summary")
async def get_risk_summary(db: Session = Depends(get_db)):
    """Get summary of all inventory risks"""
    service = InventoryRiskService(db)
    summary = service.get_risk_summary()
    
    return {
        "status": "success",
        "data": summary
    }


@router.post("/recommendations")
async def generate_recommendations(db: Session = Depends(get_db)):
    """Generate reorder recommendations"""
    service = InventoryRiskService(db)
    recommendations = service.generate_reorder_recommendations()
    
    return {
        "status": "success",
        "data": recommendations
    }


@router.get("/recommendations")
async def get_recommendations(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get pending reorder recommendations"""
    service = InventoryRiskService(db)
    recommendations = service.get_recommendations(category)
    
    return {
        "status": "success",
        "count": len(recommendations),
        "data": recommendations
    }
