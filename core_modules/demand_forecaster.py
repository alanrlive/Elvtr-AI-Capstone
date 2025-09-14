# demand_forecaster.py
# Advanced demand forecasting using Prophet

import pandas as pd
import numpy as np
from prophet import Prophet
import warnings
import os
warnings.filterwarnings('ignore')

class DemandForecaster:
    """Advanced demand forecasting engine"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.forecast_cache = {}
        
    def prepare_data(self, df, item_id=None, date_col='Date', sales_col='Sales'):
        """Prepare data for Prophet forecasting"""
        
        if item_id:
            # Filter for specific item
            item_data = df[df['Item_Identifier'] == item_id].copy()
        else:
            # Use all data aggregated
            item_data = df.copy()
            
        # Aggregate daily sales
        if item_id:
            daily_sales = item_data.groupby(date_col)[sales_col].sum().reset_index()
        else:
            daily_sales = item_data.groupby(date_col)[sales_col].sum().reset_index()
        
        # Prophet requires specific column names
        prophet_data = daily_sales.rename(columns={date_col: 'ds', sales_col: 'y'})
        
        return prophet_data
    
    def build_model(self, config=None):
        """Build and configure Prophet model"""
        
        # Default configuration
        default_config = {
            'yearly_seasonality': True,
            'weekly_seasonality': True,
            'daily_seasonality': False,
            'changepoint_prior_scale': 0.05,
            'seasonality_prior_scale': 10.0,
            'holidays_prior_scale': 10.0
        }
        
        if config:
            default_config.update(config)
            
        self.model = Prophet(**default_config)
        
        # Add custom seasonalities for retail
        self.model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        
        # Add holiday effects for retail (if needed)
        self._add_retail_holidays()
        
        return self.model
    
    def _add_retail_holidays(self):
        """Add retail-specific holiday effects"""
        
        # Define major retail holidays
        holidays = pd.DataFrame({
            'holiday': ['black_friday', 'cyber_monday', 'christmas', 'new_year'],
            'ds': pd.to_datetime([
                '2024-11-25', '2024-11-28', '2024-12-25', '2024-01-01'
            ]),
            'lower_window': [0, 0, -5, -2],
            'upper_window': [3, 1, 2, 3],
        })
        
        # Note: Prophet holidays need to be added before fitting
        # This is a simplified version - in production you'd add multi-year holidays
        
    def train(self, train_data):
        """Train the forecasting model"""
        
        if self.model is None:
            self.build_model()
            
        print("🔮 Training demand forecasting model...")
        self.model.fit(train_data)
        self.is_trained = True
        print("✅ Model training complete!")
        
        return self.model
    
    def forecast(self, periods=30, include_history=True):
        """Generate demand forecasts"""
        
        if not self.is_trained:
            raise ValueError("Model must be trained before forecasting")
            
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=periods, include_history=include_history)
        
        # Generate forecast
        forecast = self.model.predict(future)
        
        # Ensure non-negative predictions
        forecast['yhat'] = forecast['yhat'].clip(lower=0)
        forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
        forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)
        
        return forecast
    
    def get_forecast_for_date(self, target_date, forecast_df=None):
        """Get forecast for a specific date"""
        
        if forecast_df is None:
            forecast_df = self.forecast(periods=365)  # Generate long forecast
            
        # Find the forecast for the target date
        target_forecast = forecast_df[forecast_df['ds'] == target_date]
        
        if len(target_forecast) == 0:
            # If exact date not found, find the closest
            forecast_df['date_diff'] = abs((forecast_df['ds'] - target_date).dt.days)
            closest = forecast_df.loc[forecast_df['date_diff'].idxmin()]
            return max(0, closest['yhat'])
        else:
            return max(0, target_forecast.iloc[0]['yhat'])
    
    def evaluate_model(self, test_data):
        """Evaluate model performance on test data"""
        
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
            
        # Generate predictions for test period
        test_forecast = self.model.predict(test_data)
        
        # Calculate metrics
        actual = test_data['y'].values
        predicted = test_forecast['yhat'].values
        
        mae = np.mean(np.abs(actual - predicted))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        
        metrics = {
            'MAE': mae,
            'MAPE': mape,
            'RMSE': rmse,
            'R2': np.corrcoef(actual, predicted)[0, 1] ** 2
        }
        
        return metrics
    
    def get_trend_analysis(self, forecast_df):
        """Analyze trends from forecast data"""
        
        # Extract trend component
        trend = forecast_df[['ds', 'trend']].copy()
        
        # Calculate trend direction
        trend_slope = np.polyfit(range(len(trend)), trend['trend'], 1)[0]
        
        # Seasonal analysis
        if 'yearly' in forecast_df.columns:
            yearly_peak = forecast_df['yearly'].max()
            yearly_low = forecast_df['yearly'].min()
            seasonal_amplitude = yearly_peak - yearly_low
        else:
            seasonal_amplitude = 0
            
        analysis = {
            'trend_slope': trend_slope,
            'trend_direction': 'increasing' if trend_slope > 0 else 'decreasing',
            'seasonal_amplitude': seasonal_amplitude,
            'forecast_mean': forecast_df['yhat'].mean(),
            'forecast_std': forecast_df['yhat'].std()
        }
        
        return analysis
    
    def save_model(self, filepath):
        """Save trained model"""
        
        if not self.is_trained:
            raise ValueError("No trained model to save")
            
        # Prophet models need to be saved using pickle or joblib
        import pickle
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
            
        print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load pre-trained model"""
        
        import pickle
        
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
            
        self.is_trained = True
        print(f"✅ Model loaded from {filepath}")