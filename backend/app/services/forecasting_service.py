"""Forecasting Service"""
import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.ml.forecasting import MultiProductForecaster, calculate_forecast_metrics
from app.models import Forecast, SalesData, Product


class ForecastingService:
    """Service layer for forecasting operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.forecaster = MultiProductForecaster()
    
    def get_product_sales_history(self, product_id: str, days: int = 90) -> np.ndarray:
        """Retrieve sales history for a product"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        sales = self.db.query(SalesData).filter(
            SalesData.product_id == product_id,
            SalesData.date >= start_date
        ).order_by(SalesData.date).all()
        
        # If no sales data, return random data for demo
        if not sales:
            return np.random.randint(5, 50, days)
        
        # Fill missing dates with zero sales
        sales_dict = {s.date.date(): s.quantity_sold for s in sales}
        full_history = []
        current_date = start_date.date()
        
        for i in range(days):
            full_history.append(sales_dict.get(current_date, 0))
            current_date = (datetime.strptime(str(current_date), '%Y-%m-%d') + timedelta(days=1)).date()
        
        return np.array(full_history, dtype=float)
    
    def train_product_forecaster(self, product_id: str, days: int = 90) -> bool:
        """Train forecaster for a product"""
        try:
            sales_data = self.get_product_sales_history(product_id, days)
            if len(sales_data) < 10:
                print(f"Insufficient data for {product_id}")
                return False
            
            self.forecaster.fit_product(product_id, sales_data)
            return True
        except Exception as e:
            print(f"Error training forecaster for {product_id}: {e}")
            return False
    
    def forecast_product_demand(self, product_id: str, days: int = 7) -> Optional[Dict]:
        """Forecast demand for a product"""
        try:
            # Train if not already trained
            if product_id not in self.forecaster.forecasters:
                self.train_product_forecaster(product_id)
            
            forecast = self.forecaster.forecast_product(product_id, days)
            if not forecast:
                return None
            
            # Save forecast to database
            forecast_record = Forecast(
                product_id=product_id,
                forecast_date=datetime.utcnow(),
                forecast_days=days,
                hybrid_forecast=json.dumps(forecast['hybrid'].tolist()),
                arima_forecast=json.dumps(forecast['arima'].tolist()),
                gb_forecast=json.dumps(forecast['gradient_boosting'].tolist())
            )
            self.db.add(forecast_record)
            self.db.commit()
            
            return {
                'product_id': product_id,
                'forecast_date': forecast_record.forecast_date.isoformat(),
                'days': days,
                'hybrid_forecast': forecast['hybrid'].tolist(),
                'arima_forecast': forecast['arima'].tolist(),
                'gradient_boosting': forecast['gradient_boosting'].tolist()
            }
        except Exception as e:
            print(f"Error forecasting {product_id}: {e}")
            return None
    
    def forecast_multiple_products(self, product_ids: List[str], days: int = 7) -> List[Dict]:
        """Forecast for multiple products"""
        results = []
        for product_id in product_ids:
            forecast = self.forecast_product_demand(product_id, days)
            if forecast:
                results.append(forecast)
        return results
    
    def evaluate_forecast(self, product_id: str, forecast_id: Optional[int] = None) -> Optional[Dict]:
        """Evaluate forecast accuracy against actual sales"""
        try:
            # Get recent forecast
            forecast_record = self.db.query(Forecast).filter(
                Forecast.product_id == product_id
            ).order_by(Forecast.forecast_date.desc()).first()
            
            if not forecast_record:
                return None
            
            # Get actual sales since forecast
            actual_sales_data = self.get_product_sales_history(product_id, days=forecast_record.forecast_days)
            recent_sales = actual_sales_data[-forecast_record.forecast_days:]
            
            # Get forecast values
            hybrid_forecast = np.array(json.loads(forecast_record.hybrid_forecast))
            
            # Calculate metrics
            metrics = calculate_forecast_metrics(recent_sales, hybrid_forecast)
            
            return {
                'product_id': product_id,
                'forecast_date': forecast_record.forecast_date.isoformat(),
                'forecast_days': forecast_record.forecast_days,
                'actual_sales': recent_sales.tolist(),
                'forecast': hybrid_forecast.tolist(),
                'metrics': metrics
            }
        except Exception as e:
            print(f"Error evaluating forecast for {product_id}: {e}")
            return None
    
    def get_forecast_history(self, product_id: str, limit: int = 10) -> List[Dict]:
        """Get forecast history for a product"""
        forecasts = self.db.query(Forecast).filter(
            Forecast.product_id == product_id
        ).order_by(Forecast.forecast_date.desc()).limit(limit).all()
        
        return [
            {
                'forecast_date': f.forecast_date.isoformat(),
                'forecast_days': f.forecast_days,
                'hybrid_forecast': json.loads(f.hybrid_forecast),
                'arima_forecast': json.loads(f.arima_forecast),
                'gb_forecast': json.loads(f.gb_forecast)
            }
            for f in forecasts
        ]
