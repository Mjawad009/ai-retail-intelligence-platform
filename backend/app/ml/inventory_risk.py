"""
Inventory Risk Modeling
Safety stock calculation, reorder point, and stockout risk scoring
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from scipy import stats


class InventoryRiskCalculator:
    """Calculate inventory risk metrics and recommendations"""
    
    # Service level (confidence level for safety stock)
    SERVICE_LEVEL = 0.95  # 95% service level
    LEAD_TIME = 7  # days
    
    @staticmethod
    def calculate_z_score(service_level: float = 0.95) -> float:
        """Get z-score from service level"""
        return stats.norm.ppf(service_level)
    
    @staticmethod
    def calculate_safety_stock(demand_std: float, lead_time: float, 
                              service_level: float = 0.95) -> float:
        """
        Calculate safety stock using standard deviation method
        Safety Stock = Z-score * std(demand) * sqrt(lead_time)
        """
        z_score = InventoryRiskCalculator.calculate_z_score(service_level)
        return z_score * demand_std * np.sqrt(lead_time)
    
    @staticmethod
    def calculate_reorder_point(mean_demand: float, lead_time: float, 
                               safety_stock: float) -> float:
        """
        Calculate reorder point
        ROP = (Average Daily Demand * Lead Time) + Safety Stock
        """
        return (mean_demand * lead_time) + safety_stock
    
    @staticmethod
    def calculate_stockout_risk(current_stock: float, reorder_point: float, 
                               safety_stock: float) -> float:
        """
        Calculate stockout risk score (0-100)
        Higher score = higher risk
        """
        if current_stock < reorder_point:
            risk_score = min(100.0, 100 * (1 - (current_stock / reorder_point)))
        else:
            risk_percentage = (current_stock - safety_stock) / (reorder_point - safety_stock + 1)
            risk_score = max(0.0, 50 * (1 - risk_percentage))
        
        return float(risk_score)
    
    @staticmethod
    def calculate_eoq(annual_demand: float, ordering_cost: float, 
                     holding_cost: float) -> float:
        """
        Calculate Economic Order Quantity (EOQ)
        EOQ = sqrt(2 * D * S / H)
        D = annual demand, S = order cost, H = holding cost
        """
        if holding_cost <= 0:
            return 0
        return np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)


class InventoryRiskModel:
    """Comprehensive inventory risk analysis"""
    
    def __init__(self, lead_time: int = 7, service_level: float = 0.95):
        self.lead_time = lead_time
        self.service_level = service_level
        self.calculator = InventoryRiskCalculator()
    
    def analyze_product_inventory(self, product_data: Dict) -> Dict:
        """
        Analyze inventory risk for a product
        
        Expected keys in product_data:
        - current_stock: current inventory level
        - daily_demand_mean: average daily demand
        - daily_demand_std: std dev of daily demand
        - unit_cost: cost per unit
        - holding_cost_rate: annual holding cost as % of unit cost
        - order_cost: cost to place an order
        - recent_sales: list of recent daily sales (optional)
        """
        current_stock = product_data.get('current_stock', 0)
        demand_mean = product_data.get('daily_demand_mean', 0)
        demand_std = product_data.get('daily_demand_std', max(demand_mean * 0.1, 1))
        unit_cost = product_data.get('unit_cost', 0)
        holding_cost_rate = product_data.get('holding_cost_rate', 0.2)
        order_cost = product_data.get('order_cost', 50)
        
        # Calculate holding cost
        holding_cost = unit_cost * holding_cost_rate
        
        # Calculate safety stock
        safety_stock = self.calculator.calculate_safety_stock(
            demand_std, 
            self.lead_time, 
            self.service_level
        )
        
        # Calculate reorder point
        reorder_point = self.calculator.calculate_reorder_point(
            demand_mean, 
            self.lead_time, 
            safety_stock
        )
        
        # Calculate stockout risk
        stockout_risk = self.calculator.calculate_stockout_risk(
            current_stock, 
            reorder_point, 
            safety_stock
        )
        
        # Calculate EOQ
        annual_demand = demand_mean * 365
        eoq = self.calculator.calculate_eoq(
            annual_demand, 
            order_cost, 
            holding_cost
        )
        
        # Calculate recommended order quantity
        if current_stock < reorder_point:
            recommended_order = max(eoq, reorder_point - current_stock)
        else:
            recommended_order = eoq
        
        # Days until stockout (approximation)
        days_to_stockout = (current_stock / (demand_mean + 0.1)) if demand_mean > 0 else float('inf')
        
        return {
            'product_id': product_data.get('product_id', 'unknown'),
            'current_stock': float(current_stock),
            'daily_demand_mean': float(demand_mean),
            'daily_demand_std': float(demand_std),
            'safety_stock': float(safety_stock),
            'reorder_point': float(reorder_point),
            'stockout_risk_score': float(stockout_risk),
            'stockout_risk_level': self._risk_level(stockout_risk),
            'recommended_order_qty': float(max(0, recommended_order)),
            'economic_order_qty': float(eoq),
            'days_to_potential_stockout': float(min(days_to_stockout, 1000)),
            'reorder_recommended': current_stock < reorder_point,
            'critical_alert': stockout_risk > 70
        }
    
    def analyze_multiple_products(self, products_data: List[Dict]) -> List[Dict]:
        """Analyze inventory for multiple products"""
        results = []
        for product_data in products_data:
            try:
                analysis = self.analyze_product_inventory(product_data)
                results.append(analysis)
            except Exception as e:
                print(f"Error analyzing product {product_data.get('product_id')}: {e}")
        return results
    
    @staticmethod
    def _risk_level(risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score < 20:
            return 'low'
        elif risk_score < 50:
            return 'medium'
        elif risk_score < 70:
            return 'high'
        else:
            return 'critical'


class ReorderRecommendationEngine:
    """Generate automated reorder recommendations"""
    
    def __init__(self, lead_time: int = 7):
        self.lead_time = lead_time
        self.risk_model = InventoryRiskModel(lead_time=lead_time)
    
    def generate_recommendations(self, products_data: List[Dict]) -> Dict:
        """Generate reorder recommendations for products"""
        analyses = self.risk_model.analyze_multiple_products(products_data)
        
        recommendations = {
            'immediate': [],  # Stock immediately
            'urgent': [],      # Within 1-2 days
            'soon': [],        # Within 1 week
            'optimal': [],     # Based on EOQ
            'no_action': []    # No reorder needed
        }
        
        for analysis in analyses:
            if analysis['critical_alert']:
                recommendations['immediate'].append({
                    'product_id': analysis['product_id'],
                    'reason': 'Critical stockout risk',
                    'suggested_quantity': analysis['recommended_order_qty'],
                    'priority': 1
                })
            elif analysis['reorder_recommended']:
                days_to_stockout = analysis['days_to_potential_stockout']
                if days_to_stockout < 3:
                    recommendations['urgent'].append({
                        'product_id': analysis['product_id'],
                        'reason': f'Stockout in ~{days_to_stockout:.1f} days',
                        'suggested_quantity': analysis['recommended_order_qty'],
                        'priority': 2
                    })
                else:
                    recommendations['soon'].append({
                        'product_id': analysis['product_id'],
                        'reason': 'Approaching reorder point',
                        'suggested_quantity': analysis['recommended_order_qty'],
                        'priority': 3
                    })
            elif analysis['stockout_risk_score'] > 30:
                recommendations['optimal'].append({
                    'product_id': analysis['product_id'],
                    'reason': 'Optimize stock level',
                    'suggested_quantity': analysis['economic_order_qty'],
                    'priority': 4
                })
            else:
                recommendations['no_action'].append({
                    'product_id': analysis['product_id'],
                    'reason': 'Stock level adequate',
                    'priority': 5
                })
        
        # Sort by priority
        for category in recommendations:
            recommendations[category].sort(key=lambda x: x.get('priority', 999))
        
        return recommendations
