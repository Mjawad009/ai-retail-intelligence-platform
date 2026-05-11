"""Inventory Risk Service"""
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.ml.inventory_risk import InventoryRiskModel, ReorderRecommendationEngine
from app.models import InventoryLevel, RiskAnalysis, ReorderRecommendation, Product


class InventoryRiskService:
    """Service layer for inventory risk management"""
    
    def __init__(self, db: Session, lead_time: int = 7):
        self.db = db
        self.lead_time = lead_time
        self.risk_model = InventoryRiskModel(lead_time=lead_time)
        self.reorder_engine = ReorderRecommendationEngine(lead_time=lead_time)
    
    def get_product_demand_stats(self, product_id: str, days: int = 30) -> Dict:
        """Calculate demand statistics for a product"""
        from app.models import SalesData
        import numpy as np
        from datetime import timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        sales = self.db.query(SalesData).filter(
            SalesData.product_id == product_id,
            SalesData.date >= start_date
        ).all()
        
        if not sales:
            # Return default stats
            return {
                'mean_demand': 20.0,
                'std_demand': 5.0,
                'total_sales': 0
            }
        
        quantities = [s.quantity_sold for s in sales]
        
        return {
            'mean_demand': float(np.mean(quantities)) if quantities else 0,
            'std_demand': float(np.std(quantities)) if quantities else 0,
            'total_sales': float(sum(quantities))
        }
    
    def analyze_product_risk(self, product_id: str) -> Optional[Dict]:
        """Analyze inventory risk for a product"""
        try:
            # Get product info
            product = self.db.query(Product).filter(
                Product.product_id == product_id
            ).first()
            
            if not product:
                return None
            
            # Get inventory level
            inventory = self.db.query(InventoryLevel).filter(
                InventoryLevel.product_id == product_id
            ).first()
            
            if not inventory:
                return None
            
            # Get demand stats
            demand_stats = self.get_product_demand_stats(product_id)
            
            # Prepare product data for analysis
            product_data = {
                'product_id': product_id,
                'current_stock': inventory.current_stock,
                'daily_demand_mean': demand_stats['mean_demand'],
                'daily_demand_std': demand_stats['std_demand'],
                'unit_cost': product.unit_cost,
                'holding_cost_rate': product.holding_cost_rate,
                'order_cost': product.order_cost
            }
            
            # Analyze
            analysis = self.risk_model.analyze_product_inventory(product_data)
            
            # Save to database
            risk_record = RiskAnalysis(
                product_id=product_id,
                analysis_date=datetime.utcnow(),
                current_stock=analysis['current_stock'],
                safety_stock=analysis['safety_stock'],
                reorder_point=analysis['reorder_point'],
                stockout_risk_score=analysis['stockout_risk_score'],
                stockout_risk_level=analysis['stockout_risk_level'],
                recommended_order_qty=analysis['recommended_order_qty'],
                days_to_stockout=analysis['days_to_potential_stockout'],
                reorder_recommended=analysis['reorder_recommended'],
                critical_alert=analysis['critical_alert']
            )
            self.db.add(risk_record)
            self.db.commit()
            
            return analysis
        except Exception as e:
            print(f"Error analyzing risk for {product_id}: {e}")
            return None
    
    def analyze_all_products(self) -> List[Dict]:
        """Analyze risk for all products"""
        products = self.db.query(Product).all()
        results = []
        
        for product in products:
            analysis = self.analyze_product_risk(product.product_id)
            if analysis:
                results.append(analysis)
        
        return results
    
    def get_risk_summary(self) -> Dict:
        """Get summary of all risks"""
        all_analyses = self.analyze_all_products()
        
        critical = [a for a in all_analyses if a['critical_alert']]
        high_risk = [a for a in all_analyses if a['stockout_risk_level'] == 'high']
        
        return {
            'total_products': len(all_analyses),
            'critical_alerts': len(critical),
            'high_risk_products': len(high_risk),
            'critical_products': [a['product_id'] for a in critical],
            'high_risk_products_list': [a['product_id'] for a in high_risk]
        }
    
    def generate_reorder_recommendations(self) -> Dict:
        """Generate reorder recommendations for all products"""
        try:
            all_analyses = self.analyze_all_products()
            
            # Prepare data for recommendation engine
            products_data = []
            for analysis in all_analyses:
                inventory = self.db.query(InventoryLevel).filter(
                    InventoryLevel.product_id == analysis['product_id']
                ).first()
                
                if inventory:
                    product = self.db.query(Product).filter(
                        Product.product_id == analysis['product_id']
                    ).first()
                    
                    products_data.append({
                        'product_id': analysis['product_id'],
                        'current_stock': inventory.current_stock,
                        'daily_demand_mean': analysis['daily_demand_mean'],
                        'daily_demand_std': analysis['daily_demand_std'],
                        'unit_cost': product.unit_cost if product else 0,
                        'holding_cost_rate': product.holding_cost_rate if product else 0.2,
                        'order_cost': product.order_cost if product else 50
                    })
            
            # Generate recommendations
            recommendations = self.reorder_engine.generate_recommendations(products_data)
            
            # Save recommendations to database
            for category, items in recommendations.items():
                for item in items:
                    rec = ReorderRecommendation(
                        product_id=item['product_id'],
                        recommendation_date=datetime.utcnow(),
                        category=category,
                        reason=item['reason'],
                        suggested_quantity=item['suggested_quantity'],
                        priority=item['priority']
                    )
                    self.db.add(rec)
            
            self.db.commit()
            return recommendations
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return {}
    
    def get_recommendations(self, category: Optional[str] = None) -> List[Dict]:
        """Get reorder recommendations"""
        query = self.db.query(ReorderRecommendation).filter(
            ReorderRecommendation.status == 'pending'
        )
        
        if category:
            query = query.filter(ReorderRecommendation.category == category)
        
        recs = query.order_by(ReorderRecommendation.priority).all()
        
        return [
            {
                'id': r.id,
                'product_id': r.product_id,
                'category': r.category,
                'reason': r.reason,
                'suggested_quantity': r.suggested_quantity,
                'priority': r.priority,
                'recommendation_date': r.recommendation_date.isoformat()
            }
            for r in recs
        ]
