"""Analytics API Endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import SalesData, Product, InventoryLevel
from app.utils.database import get_db
import numpy as np

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/sales-trends")
async def get_sales_trends(
    product_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get sales trends for a product"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    sales = db.query(SalesData).filter(
        SalesData.product_id == product_id,
        SalesData.date >= start_date
    ).order_by(SalesData.date).all()
    
    # Group by day
    daily_sales = {}
    for sale in sales:
        day = sale.date.date()
        if day not in daily_sales:
            daily_sales[day] = 0
        daily_sales[day] += sale.quantity_sold
    
    dates = sorted(daily_sales.keys())
    values = [daily_sales[d] for d in dates]
    
    return {
        "status": "success",
        "product_id": product_id,
        "data": {
            "dates": [str(d) for d in dates],
            "sales": values,
            "average": float(np.mean(values)) if values else 0,
            "trend": "up" if values and values[-1] > np.mean(values[:len(values)//2]) else "down"
        }
    }


@router.get("/inventory-trends")
async def get_inventory_trends(
    product_id: str = None,
    db: Session = Depends(get_db)
):
    """Get inventory trends"""
    if product_id:
        inventory = db.query(InventoryLevel).filter(
            InventoryLevel.product_id == product_id
        ).first()
        
        if not inventory:
            return {"status": "error", "message": "Product not found"}
        
        return {
            "status": "success",
            "product_id": product_id,
            "data": {
                "current_stock": inventory.current_stock,
                "reserved_stock": inventory.reserved_stock,
                "available_stock": inventory.available_stock,
                "last_update": inventory.updated_at.isoformat()
            }
        }
    else:
        # Get all products inventory
        inventories = db.query(InventoryLevel).all()
        
        total_stock = sum([i.current_stock for i in inventories])
        low_stock = len([i for i in inventories if i.current_stock < 20])
        
        return {
            "status": "success",
            "data": {
                "total_inventory_value": total_stock,
                "products_low_stock": low_stock,
                "total_products": len(inventories)
            }
        }


@router.get("/product-performance")
async def get_product_performance(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get performance metrics for all products"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    products = db.query(Product).all()
    performance = []
    
    for product in products:
        sales = db.query(SalesData).filter(
            SalesData.product_id == product.product_id,
            SalesData.date >= start_date
        ).all()
        
        total_sales = sum([s.quantity_sold for s in sales])
        total_revenue = sum([s.revenue for s in sales])
        
        inventory = db.query(InventoryLevel).filter(
            InventoryLevel.product_id == product.product_id
        ).first()
        
        performance.append({
            "product_id": product.product_id,
            "product_name": product.name,
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "current_stock": inventory.current_stock if inventory else 0,
            "avg_daily_sales": total_sales / days if days > 0 else 0
        })
    
    # Sort by revenue
    performance.sort(key=lambda x: x['total_revenue'], reverse=True)
    
    return {
        "status": "success",
        "count": len(performance),
        "data": performance
    }


@router.get("/dashboard-summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary data"""
    # Total products
    total_products = db.query(Product).count()
    
    # Total inventory
    inventories = db.query(InventoryLevel).all()
    total_inventory = sum([i.current_stock for i in inventories])
    
    # Recent sales (last 7 days)
    start_date = datetime.utcnow() - timedelta(days=7)
    recent_sales = db.query(SalesData).filter(
        SalesData.date >= start_date
    ).all()
    total_recent_sales = sum([s.quantity_sold for s in recent_sales])
    total_recent_revenue = sum([s.revenue for s in recent_sales])
    
    return {
        "status": "success",
        "data": {
            "total_products": total_products,
            "total_inventory": float(total_inventory),
            "recent_sales_quantity": float(total_recent_sales),
            "recent_sales_revenue": float(total_recent_revenue),
            "low_stock_alerts": len([i for i in inventories if i.current_stock < 20])
        }
    }
