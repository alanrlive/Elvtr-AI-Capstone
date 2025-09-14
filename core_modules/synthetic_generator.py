# synthetic_generator.py
# Generate synthetic data with engineered demo scenarios

import pandas as pd
import numpy as np

class EnhancedSyntheticGenerator:
    """Generate synthetic data using extracted real patterns"""
    
    def __init__(self, real_patterns):
        self.patterns = real_patterns
        
    def generate_demo_scenarios(self, category='Electronics', start_date='2024-01-01', days=365):
        """Generate synthetic data with engineered demo scenarios"""
        
        dates = pd.date_range(start_date, periods=days, freq='D')
        pattern = self.patterns[category]
        
        scenarios = []
        
        for date in dates:
            base_demand = pattern['base_level']
            yearly_effect = self._apply_yearly_seasonality(date, pattern)
            weekly_effect = self._apply_weekly_seasonality(date, pattern)
            
            realistic_demand = base_demand * yearly_effect * weekly_effect
            scenario_multiplier, scenario_name = self._apply_demo_scenarios(date)
            
            noise = np.random.normal(0, pattern['volatility'] * realistic_demand)
            final_demand = max(0, realistic_demand * scenario_multiplier + noise)
            
            scenarios.append({
                'Date': date,
                'Item_Identifier': f"{category}_DEMO_ITEM",
                'Item_Category': category,
                'Sales': final_demand,
                'Base_Demand': realistic_demand,
                'Scenario_Effect': scenario_multiplier,
                'Scenario_Name': scenario_name,
                'Item_MRP': 50.0,
                'Outlet_Type': 'Supermarket Type1'
            })
        
        return pd.DataFrame(scenarios)
    
    def _apply_yearly_seasonality(self, date, pattern):
        """Apply realistic yearly seasonality"""
        base_seasonal = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
        if date.month in pattern['seasonal_peaks']:
            base_seasonal *= 1.4
        return base_seasonal
    
    def _apply_weekly_seasonality(self, date, pattern):
        """Apply realistic weekly patterns"""
        if date.weekday() == 5:  # Saturday
            return 1.3
        elif date.weekday() == 6:  # Sunday
            return 1.1
        elif date.weekday() == 0:  # Monday
            return 0.8
        else:
            return 1.0
    
    def _apply_demo_scenarios(self, date):
        """Add engineered scenarios perfect for demos"""
        
        if date.month == 3 and 15 <= date.day <= 17:
            return 3.5, "Viral_Social_Media_Boost"
        elif date.month == 5 and 10 <= date.day <= 20:
            return 2.2, "Competitor_Stockout_Benefit"
        elif date.month == 7 and 1 <= date.day <= 14:
            return 0.3, "Supply_Chain_Disruption"
        elif date.month == 9 and 8 <= date.day <= 12:
            return 4.0, "Celebrity_Endorsement_Spike"
        elif date.month == 11 and 1 <= date.day <= 10:
            return 0.6, "Economic_Downturn_Effect"
        elif date.month == 11 and 24 <= date.day <= 27:
            return 5.0, "Black_Friday_Mega_Event"
        elif date.month == 1 and 2 <= date.day <= 15:
            return 0.4, "Post_Holiday_Clearance"
        else:
            return 1.0, "Normal_Operations"
            
    def get_scenario_descriptions(self):
        """Return descriptions of all demo scenarios for documentation"""
        return {
            "Viral_Social_Media_Boost": {
                "description": "Sudden viral social media event drives 3.5x demand spike",
                "period": "March 15-17",
                "multiplier": 3.5,
                "purpose": "Test agent's ability to handle unexpected massive demand"
            },
            "Celebrity_Endorsement_Spike": {
                "description": "Celebrity endorsement creates 4x demand increase",
                "period": "September 8-12", 
                "multiplier": 4.0,
                "purpose": "Demonstrate scalability and rapid response capabilities"
            },
            "Black_Friday_Mega_Event": {
                "description": "Black Friday creates 5x demand surge",
                "period": "November 24-27",
                "multiplier": 5.0,
                "purpose": "Show handling of predictable but extreme seasonal events"
            },
            "Supply_Chain_Disruption": {
                "description": "Supply issues reduce demand to 30% of normal",
                "period": "July 1-14",
                "multiplier": 0.3,
                "purpose": "Test conservative inventory management during uncertainty"
            },
            "Economic_Downturn_Effect": {
                "description": "Economic conditions reduce demand to 60%",
                "period": "November 1-10", 
                "multiplier": 0.6,
                "purpose": "Demonstrate risk management and cost optimization"
            },
            "Competitor_Stockout_Benefit": {
                "description": "Competitor stockout increases our demand by 2.2x",
                "period": "May 10-20",
                "multiplier": 2.2,
                "purpose": "Show opportunity capture and market share gains"
            },
            "Post_Holiday_Clearance": {
                "description": "Post-holiday period with 40% of normal demand",
                "period": "January 2-15",
                "multiplier": 0.4,
                "purpose": "Test inventory reduction and clearance strategies"
            }
        }