"""
Demand Forecasting Module
Combines ARIMA and Gradient Boosting for multi-product predictions
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from statsmodels.tsa.arima.model import ARIMA
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class ArimaForecaster:
    """ARIMA Time-Series Forecasting"""
    
    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1)):
        self.order = order
        self.model = None
        self.fitted = False
    
    def fit(self, series: np.ndarray) -> None:
        """Fit ARIMA model"""
        try:
            self.model = ARIMA(series, order=self.order)
            self.model = self.model.fit()
            self.fitted = True
        except Exception as e:
            print(f"ARIMA fitting error: {e}")
            self.fitted = False
    
    def forecast(self, steps: int = 7) -> np.ndarray:
        """Generate forecasts"""
        if not self.fitted:
            raise ValueError("Model not fitted")
        try:
            forecast = self.model.get_forecast(steps=steps)
            return forecast.predicted_mean.values
        except Exception as e:
            print(f"ARIMA forecast error: {e}")
            return np.zeros(steps)


class GradientBoostingForecaster:
    """Gradient Boosting Forecasting with lagged features"""
    
    def __init__(self, n_lags: int = 7, n_estimators: int = 100):
        self.n_lags = n_lags
        self.model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.fitted = False
        self.last_values = None
    
    def _create_lagged_features(self, series: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create lagged features from time series"""
        X, y = [], []
        for i in range(len(series) - self.n_lags):
            X.append(series[i:i + self.n_lags])
            y.append(series[i + self.n_lags])
        return np.array(X), np.array(y)
    
    def fit(self, series: np.ndarray) -> None:
        """Fit gradient boosting model"""
        try:
            X, y = self._create_lagged_features(series)
            if len(X) == 0:
                raise ValueError("Insufficient data for lagged features")
            
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.last_values = series[-self.n_lags:]
            self.fitted = True
        except Exception as e:
            print(f"GB fitting error: {e}")
            self.fitted = False
    
    def forecast(self, steps: int = 7) -> np.ndarray:
        """Generate forecasts"""
        if not self.fitted:
            raise ValueError("Model not fitted")
        
        forecasts = []
        current_values = self.last_values.copy()
        
        for _ in range(steps):
            features = current_values[-self.n_lags:].reshape(1, -1)
            features_scaled = self.scaler.transform(features)
            next_pred = self.model.predict(features_scaled)[0]
            forecasts.append(next_pred)
            current_values = np.append(current_values, next_pred)
        
        return np.array(forecasts)


class HybridForecaster:
    """Hybrid forecasting combining ARIMA and Gradient Boosting"""
    
    def __init__(self, arima_weight: float = 0.4, gb_weight: float = 0.6):
        self.arima = ArimaForecaster()
        self.gb = GradientBoostingForecaster()
        self.arima_weight = arima_weight
        self.gb_weight = gb_weight
        self.fitted = False
    
    def fit(self, series: np.ndarray) -> None:
        """Fit both models"""
        if len(series) < 10:
            raise ValueError("Need at least 10 data points")
        
        self.arima.fit(series)
        self.gb.fit(series)
        self.fitted = True
    
    def forecast(self, steps: int = 7) -> Dict[str, np.ndarray]:
        """Generate hybrid forecast"""
        if not self.fitted:
            raise ValueError("Model not fitted")
        
        arima_pred = self.arima.forecast(steps) if self.arima.fitted else np.zeros(steps)
        gb_pred = self.gb.forecast(steps) if self.gb.fitted else np.zeros(steps)
        
        # Weighted ensemble
        hybrid_pred = (self.arima_weight * arima_pred + 
                      self.gb_weight * gb_pred)
        
        return {
            'hybrid': np.maximum(hybrid_pred, 0),  # No negative predictions
            'arima': np.maximum(arima_pred, 0),
            'gradient_boosting': np.maximum(gb_pred, 0)
        }


class MultiProductForecaster:
    """Manage forecasting for multiple products"""
    
    def __init__(self):
        self.forecasters: Dict[str, HybridForecaster] = {}
        self.historical_data: Dict[str, pd.DataFrame] = {}
    
    def fit_product(self, product_id: str, sales_data: np.ndarray) -> None:
        """Fit forecaster for a specific product"""
        try:
            forecaster = HybridForecaster()
            forecaster.fit(sales_data)
            self.forecasters[product_id] = forecaster
            print(f"Product {product_id}: Forecaster fitted successfully")
        except Exception as e:
            print(f"Error fitting forecaster for product {product_id}: {e}")
    
    def forecast_product(self, product_id: str, steps: int = 7) -> Optional[Dict]:
        """Forecast for a specific product"""
        if product_id not in self.forecasters:
            return None
        
        return self.forecasters[product_id].forecast(steps)
    
    def forecast_multiple(self, products: List[str], steps: int = 7) -> Dict:
        """Forecast for multiple products"""
        results = {}
        for product_id in products:
            forecast = self.forecast_product(product_id, steps)
            if forecast:
                results[product_id] = forecast
        return results


def calculate_forecast_metrics(actual: np.ndarray, predicted: np.ndarray) -> Dict[str, float]:
    """Calculate forecast accuracy metrics"""
    mae = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    mape = np.mean(np.abs((actual - predicted) / (actual + 1))) * 100
    
    return {
        'mae': float(mae),
        'rmse': float(rmse),
        'mape': float(mape)
    }
