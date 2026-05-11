"""Database Models using SQLAlchemy"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Product(Base):
    """Product model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    unit_cost = Column(Float, default=0.0)
    holding_cost_rate = Column(Float, default=0.2)  # 20% of unit cost
    order_cost = Column(Float, default=50.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_product_id', 'product_id'),
        Index('idx_category', 'category'),
    )


class SalesData(Base):
    """Daily sales data"""
    __tablename__ = "sales_data"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String(50), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    quantity_sold = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_product_date', 'product_id', 'date'),
    )


class InventoryLevel(Base):
    """Current inventory levels"""
    __tablename__ = "inventory_levels"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String(50), unique=True, nullable=False, index=True)
    current_stock = Column(Float, nullable=False, default=0.0)
    reserved_stock = Column(Float, default=0.0)
    available_stock = Column(Float, default=0.0)
    last_restock_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Forecast(Base):
    """Forecast records"""
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String(50), nullable=False, index=True)
    forecast_date = Column(DateTime, nullable=False)
    forecast_days = Column(Integer, default=7)
    hybrid_forecast = Column(Text)  # JSON array
    arima_forecast = Column(Text)   # JSON array
    gb_forecast = Column(Text)      # JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_product_forecast_date', 'product_id', 'forecast_date'),
    )


class RiskAnalysis(Base):
    """Inventory risk analysis results"""
    __tablename__ = "risk_analysis"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String(50), nullable=False, index=True)
    analysis_date = Column(DateTime, nullable=False)
    current_stock = Column(Float)
    safety_stock = Column(Float)
    reorder_point = Column(Float)
    stockout_risk_score = Column(Float)
    stockout_risk_level = Column(String(20))  # low, medium, high, critical
    recommended_order_qty = Column(Float)
    days_to_stockout = Column(Float)
    reorder_recommended = Column(Boolean, default=False)
    critical_alert = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_product_analysis_date', 'product_id', 'analysis_date'),
    )


class ReorderRecommendation(Base):
    """Reorder recommendations"""
    __tablename__ = "reorder_recommendations"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String(50), nullable=False, index=True)
    recommendation_date = Column(DateTime, nullable=False)
    category = Column(String(50))  # immediate, urgent, soon, optimal
    reason = Column(String(255))
    suggested_quantity = Column(Float)
    priority = Column(Integer)
    status = Column(String(50), default='pending')  # pending, ordered, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_product_date_status', 'product_id', 'recommendation_date', 'status'),
    )


class AnalyticsQuery(Base):
    """Store analytics queries for assistant"""
    __tablename__ = "analytics_queries"
    
    id = Column(Integer, primary_key=True)
    query_text = Column(Text, nullable=False)
    query_type = Column(String(50))  # trend, risk, forecast, etc.
    result = Column(Text)  # JSON result
    created_at = Column(DateTime, default=datetime.utcnow)
