# streaming_production/services/data_generator.py
# Streaming data generator for production agent service

import requests
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../core_modules'))

from pattern_extractor import RealPatternExtractor
from synthetic_generator import EnhancedSyntheticGenerator

class StreamingDataGenerator:
    """Generate streaming data for the production agent service"""
    
    def __init__(self, agent_service_url='http://localhost:5001'):
        self.agent_service_url = agent_service_url
        self.current_day = 0
        self.start_date = datetime(2024, 7, 1)  # Start fresh simulation
        
        # Initialize pattern generation
        self.setup_data_patterns()
        
        # Generate scenario calendar
        self.scenario_calendar = self.create_scenario_calendar()
        
        print("🎯 Streaming Data Generator Initialized")
        print(f"📡 Target Agent Service: {self.agent_service_url}")
        print(f"📅 Starting from: {self.start_date.strftime('%Y-%m-%d')}")
        print(f"⚡ Will generate data every 10 seconds")
        
    def setup_data_patterns(self):
        """Setup data generation patterns"""
        
        print("🔍 Setting up realistic data patterns...")
        
        # Extract patterns for realistic generation
        extractor = RealPatternExtractor()
        real_data = extractor.load_walmart_kaggle_data()
        patterns = extractor.extract_patterns(real_data)
        
        # Initialize synthetic generator with real patterns
        self.generator = EnhancedSyntheticGenerator(patterns)
        self.electronics_pattern = patterns['Electronics']
        
        print("✅ Data patterns ready")
    
    def create_scenario_calendar(self):
        """Create a calendar of upcoming scenarios for exciting demos"""
        
        scenarios = {}
        
        # Plan exciting scenarios for demo
        base_date = self.start_date
        
        # Day 5: Competitor stockout
        scenarios[5] = {
            'name': 'Competitor_Stockout_Benefit',
            'multiplier': 2.2,
            'duration': 3
        }
        
        # Day 12: Viral social media event
        scenarios[12] = {
            'name': 'Viral_Social_Media_Boost', 
            'multiplier': 3.5,
            'duration': 2
        }
        
        # Day 20: Supply chain disruption
        scenarios[20] = {
            'name': 'Supply_Chain_Disruption',
            'multiplier': 0.3,
            'duration': 5
        }
        
        # Day 30: Celebrity endorsement
        scenarios[30] = {
            'name': 'Celebrity_Endorsement_Spike',
            'multiplier': 4.0,
            'duration': 3
        }
        
        # Day 45: Economic downturn
        scenarios[45] = {
            'name': 'Economic_Downturn_Effect',
            'multiplier': 0.6,
            'duration': 7
        }
        
        return scenarios
    
    def generate_daily_data(self):
        """Generate one day's worth of realistic data"""
        
        self.current_day += 1
        current_date = self.start_date + timedelta(days=self.current_day - 1)
        
        # Base demand calculation using real patterns
        base_demand = self.electronics_pattern['base_level']
        
        # Apply realistic seasonality
        yearly_effect = 1 + 0.3 * np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365)
        
        # Weekend effects
        weekend_effect = 1.0
        if current_date.weekday() == 5:  # Saturday
            weekend_effect = 1.3
        elif current_date.weekday() == 6:  # Sunday
            weekend_effect = 1.1
        elif current_date.weekday() == 0:  # Monday
            weekend_effect = 0.8
        
        # Calculate realistic demand
        realistic_demand = base_demand * yearly_effect * weekend_effect
        
        # Check for special scenarios
        scenario_name = 'Normal_Operations'
        scenario_multiplier = 1.0
        
        for day, scenario in self.scenario_calendar.items():
            if day <= self.current_day < day + scenario['duration']:
                scenario_name = scenario['name']
                scenario_multiplier = scenario['multiplier']
                break
        
        # Apply scenario effect
        final_demand = realistic_demand * scenario_multiplier
        
        # Add realistic noise
        noise = np.random.normal(0, self.electronics_pattern['volatility'] * realistic_demand)
        actual_sales = max(0, final_demand + noise)
        
        # Create data packet
        daily_data = {
            'date': current_date.strftime('%Y-%m-%d'),
            'sales': round(actual_sales, 2),
            'predicted_demand': round(final_demand, 2),
            'scenario': scenario_name,
            'base_demand': round(realistic_demand, 2),
            'scenario_multiplier': scenario_multiplier,
            'day_of_week': current_date.strftime('%A'),
            'is_weekend': current_date.weekday() >= 5
        }
        
        return daily_data
    
    def send_data_to_agent(self, daily_data):
        """Send data to the agent service"""
        
        try:
            response = requests.post(
                f"{self.agent_service_url}/api/process-day",
                json=daily_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                print(f"❌ Agent service error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to agent service at {self.agent_service_url}")
            print("💡 Make sure the agent service is running!")
            return None
        except Exception as e:
            print(f"❌ Error sending data: {e}")
            return None
    
    def check_agent_service(self):
        """Check if agent service is available"""
        
        try:
            response = requests.get(f"{self.agent_service_url}/api/health", timeout=5)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
    def print_daily_summary(self, daily_data, agent_response):
        """Print summary of the day's activity"""
        
        print(f"\n📅 Day {self.current_day}: {daily_data['date']} ({daily_data['day_of_week']})")
        print(f"🛒 Sales: {daily_data['sales']:.0f} units")
        print(f"🎯 Scenario: {daily_data['scenario']}")
        
        if agent_response and agent_response.get('status') == 'success':
            decision = agent_response['agent_decision']
            print(f"🤖 Agent Action: {decision['action']}")
            print(f"📦 Current Stock: {decision['current_stock']} units")
            
            if decision['action'] == 'intelligent_reorder':
                print(f"🔄 Reorder: {decision['order_quantity']} units ({decision['urgency_level']})")
            
            metrics = agent_response['performance_metrics']
            print(f"💰 Profit: ${metrics['profit']:,.2f} | Service Level: {metrics['service_level']}%")
            
            # Special scenario announcements
            if daily_data['scenario'] != 'Normal_Operations':
                print(f"🚨 SCENARIO ACTIVE: {daily_data['scenario']} (x{daily_data['scenario_multiplier']})")
        
        print("-" * 60)
    
    def run_stream(self, max_days=100, interval_seconds=10):
        """Run the continuous data stream"""
        
        print(f"\n🚀 Starting data stream...")
        print(f"⏱️  Interval: {interval_seconds} seconds per day")
        print(f"📊 Max days: {max_days}")
        print("⏹️  Press Ctrl+C to stop")
        
        # Check agent service availability
        if not self.check_agent_service():
            print(f"❌ Agent service not available at {self.agent_service_url}")
            print("💡 Start the agent service first: python agent_service.py")
            return
        
        print("✅ Agent service is running!")
        print("\n" + "="*60)
        
        try:
            for day in range(max_days):
                # Generate daily data
                daily_data = self.generate_daily_data()
                
                # Send to agent service
                agent_response = self.send_data_to_agent(daily_data)
                
                # Print summary
                self.print_daily_summary(daily_data, agent_response)
                
                # Check for exciting scenarios coming up
                if self.current_day + 1 in self.scenario_calendar:
                    upcoming = self.scenario_calendar[self.current_day + 1]
                    print(f"🔮 TOMORROW: {upcoming['name']} begins!")
                
                # Wait for next iteration
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n⏹️  Stream stopped by user")
            print(f"📊 Generated {self.current_day} days of data")
        except Exception as e:
            print(f"\n❌ Stream error: {e}")
    
    def run_quick_demo(self, demo_days=20):
        """Run a quick demo with key scenarios"""
        
        print(f"\n🎪 Quick Demo Mode - {demo_days} days")
        print("⚡ 2 seconds per day for fast demonstration")
        
        # Override scenario calendar for quick demo
        self.scenario_calendar = {
            3: {'name': 'Competitor_Stockout_Benefit', 'multiplier': 2.2, 'duration': 2},
            8: {'name': 'Viral_Social_Media_Boost', 'multiplier': 3.5, 'duration': 2},
            15: {'name': 'Celebrity_Endorsement_Spike', 'multiplier': 4.0, 'duration': 2}
        }
        
        self.run_stream(max_days=demo_days, interval_seconds=2)

def main():
    """Main function with different run modes"""
    
    generator = StreamingDataGenerator()
    
    print("\n🎯 Choose run mode:")
    print("1. Normal stream (10 seconds per day)")
    print("2. Quick demo (2 seconds per day, 20 days)")
    print("3. Custom configuration")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        generator.run_stream(max_days=100, interval_seconds=10)
    elif choice == '2':
        generator.run_quick_demo(demo_days=20)
    elif choice == '3':
        days = int(input("Number of days: "))
        interval = int(input("Seconds per day: "))
        generator.run_stream(max_days=days, interval_seconds=interval)
    else:
        print("Invalid choice. Running default demo...")
        generator.run_quick_demo(demo_days=20)

if __name__ == '__main__':
    main()