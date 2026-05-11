"""AI Analytics Assistant
Natural language queries over sales data and inventory
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import re
import json


class AnalyticsAssistant:
    """Lightweight NLP assistant for analytics queries"""
    
    def __init__(self, db: Session):
        self.db = db
        self.patterns = {
            'stockout': r'stock\s*out|run\s*out|low.*stock|critical.*alert',
            'declining': r'declin|drop|fall|decrease|lowest',
            'forecast': r'forecast|predict|next.*week|next.*month|future',
            'top_products': r'top|best|highest|leading|most',
            'sales_trend': r'trend|sales|revenue|growth|increase',
            'inventory': r'inventory|stock|quantity|available|level'
        }
    
    def process_query(self, query: str) -> Dict:
        """Process natural language query"""
        query_lower = query.lower()
        
        # Determine query type
        query_type = self._classify_query(query_lower)
        
        # Get response based on type
        if query_type == 'stockout_risk':
            return self._handle_stockout_query()
        elif query_type == 'declining_products':
            return self._handle_declining_products_query()
        elif query_type == 'forecast':
            return self._handle_forecast_query()
        elif query_type == 'top_products':
            return self._handle_top_products_query()
        elif query_type == 'sales_trend':
            return self._handle_sales_trend_query()
        elif query_type == 'inventory':
            return self._handle_inventory_query()
        else:
            return self._handle_general_query()
    
    def _classify_query(self, query_lower: str) -> str:
        """Classify query type"""
        for pattern_type, pattern in self.patterns.items():
            if re.search(pattern, query_lower):
                if pattern_type in ['stockout', 'declining']:
                    if re.search(self.patterns['stockout'], query_lower):
                        return 'stockout_risk'
                    if re.search(self.patterns['declining'], query_lower):
                        return 'declining_products'
                return pattern_type
        return 'general'
    
    def _handle_stockout_query(self) -> Dict:
        """Handle 'Which products may stock out?' queries"""
        from app.models import RiskAnalysis
        
        critical_risks = self.db.query(RiskAnalysis).filter(
            RiskAnalysis.critical_alert == True,
            RiskAnalysis.analysis_date >= datetime.utcnow() - timedelta(hours=1)
        ).order_by(RiskAnalysis.stockout_risk_score.desc()).limit(10).all()
        
        if not critical_risks:
            # Get high risk products
            critical_risks = self.db.query(RiskAnalysis).filter(
                RiskAnalysis.stockout_risk_level == 'critical'
            ).order_by(RiskAnalysis.analysis_date.desc()).limit(10).all()
        
        products = []
        for risk in critical_risks:
            products.append({
                'product_id': risk.product_id,
                'risk_score': risk.stockout_risk_score,
                'days_to_stockout': risk.days_to_stockout,
                'current_stock': risk.current_stock,
                'recommended_order': risk.recommended_order_qty
            })
        
        return {
            'query_type': 'stockout_risk',
            'answer': f'Found {len(products)} products with critical stockout risk:',
            'products': products
        }
    
    def _handle_declining_products_query(self) -> Dict:
        """Handle 'Show top declining products' queries"""
        from app.models import SalesData, Product
        
        start_date = datetime.utcnow() - timedelta(days=30)
        
        products = self.db.query(Product).all()
        product_performance = []
        
        for product in products:
            # Get sales for first 15 days
            early_sales = self.db.query(SalesData).filter(
                SalesData.product_id == product.product_id,
                SalesData.date >= start_date,
                SalesData.date < start_date + timedelta(days=15)
            ).all()
            
            # Get sales for last 15 days
            late_sales = self.db.query(SalesData).filter(
                SalesData.product_id == product.product_id,
                SalesData.date >= start_date + timedelta(days=15)
            ).all()
            
            early_total = sum([s.quantity_sold for s in early_sales]) or 1
            late_total = sum([s.quantity_sold for s in late_sales]) or 1
            
            decline_percentage = ((early_total - late_total) / early_total) * 100 if early_total > 0 else 0
            
            if decline_percentage > 0:
                product_performance.append({
                    'product_id': product.product_id,
                    'product_name': product.name,
                    'decline_percentage': decline_percentage,
                    'early_period_sales': float(early_total),
                    'recent_period_sales': float(late_total)
                })
        
        # Sort by decline
        product_performance.sort(key=lambda x: x['decline_percentage'], reverse=True)
        top_declining = product_performance[:10]
        
        return {
            'query_type': 'declining_products',
            'answer': f'Top {len(top_declining)} declining products:',
            'products': top_declining
        }
    
    def _handle_forecast_query(self) -> Dict:
        """Handle forecast queries"""
        from app.models import Product
        
        products = self.db.query(Product).limit(3).all()
        
        return {
            'query_type': 'forecast',
            'answer': 'Next month demand forecast:',
            'products': [p.product_id for p in products],
            'forecast_days': 30,
            'note': 'Call /api/forecasting/forecast-multiple to get actual forecasts'
        }
    
    def _handle_top_products_query(self) -> Dict:
        """Handle 'top products' queries"""
        from app.models import SalesData, Product
        
        start_date = datetime.utcnow() - timedelta(days=30)
        
        products = self.db.query(Product).all()
        product_sales = []
        
        for product in products:
            sales = self.db.query(SalesData).filter(
                SalesData.product_id == product.product_id,
                SalesData.date >= start_date
            ).all()
            
            total_revenue = sum([s.revenue for s in sales])
            total_quantity = sum([s.quantity_sold for s in sales])
            
            if total_revenue > 0:
                product_sales.append({
                    'product_id': product.product_id,
                    'product_name': product.name,
                    'total_revenue': total_revenue,
                    'total_quantity': total_quantity,
                    'avg_price': total_revenue / total_quantity if total_quantity > 0 else 0
                })
        
        # Sort by revenue
        product_sales.sort(key=lambda x: x['total_revenue'], reverse=True)
        top_products = product_sales[:5]
        
        return {
            'query_type': 'top_products',
            'answer': 'Top 5 products by revenue (last 30 days):',
            'products': top_products
        }
    
    def _handle_sales_trend_query(self) -> Dict:
        """Handle sales trend queries"""
        from app.models import SalesData
        
        start_date = datetime.utcnow() - timedelta(days=30)
        
        sales = self.db.query(SalesData).filter(
            SalesData.date >= start_date
        ).all()
        
        total_sales = sum([s.quantity_sold for s in sales])
        total_revenue = sum([s.revenue for s in sales])
        
        return {
            'query_type': 'sales_trend',
            'answer': 'Sales performance (last 30 days):',
            'metrics': {
                'total_quantity_sold': total_sales,
                'total_revenue': total_revenue,
                'average_daily_revenue': total_revenue / 30
            }
        }
    
    def _handle_inventory_query(self) -> Dict:
        """Handle inventory queries"""
        from app.models import InventoryLevel
        
        inventories = self.db.query(InventoryLevel).all()
        
        low_stock = [i for i in inventories if i.current_stock < 20]
        
        return {
            'query_type': 'inventory',
            'answer': f'Found {len(low_stock)} products with low stock:',
            'low_stock_count': len(low_stock),
            'total_inventory_units': sum([i.current_stock for i in inventories]),
            'products': [
                {'product_id': i.product_id, 'current_stock': i.current_stock}
                for i in low_stock[:10]
            ]
        }
    
    def _handle_general_query(self) -> Dict:
        """Handle general queries"""
        return {
            'query_type': 'general',
            'answer': 'I can help with queries like:',
            'suggestions': [
                'Which products may stock out next week?',
                'Show top declining products',
                'Forecast next month demand',
                'What are the top selling products?',
                'Show inventory trends'
            ]
        }
