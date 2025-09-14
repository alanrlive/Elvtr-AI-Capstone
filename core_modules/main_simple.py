# main_simple.py
# Simplified main file with error handling

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def safe_import():
    """Safely import all components with error handling"""
    
    components = {}
    
    try:
        from pattern_extractor import RealPatternExtractor
        components['pattern_extractor'] = RealPatternExtractor
        print("✅ pattern_extractor loaded")
    except Exception as e:
        print(f"❌ pattern_extractor failed: {e}")
        return None
    
    try:
        from synthetic_generator import EnhancedSyntheticGenerator
        components['synthetic_generator'] = EnhancedSyntheticGenerator
        print("✅ synthetic_generator loaded")
    except Exception as e:
        print(f"❌ synthetic_generator failed: {e}")
        return None
    
    try:
        from demand_forecaster import DemandForecaster
        components['demand_forecaster'] = DemandForecaster
        print("✅ demand_forecaster loaded")
    except Exception as e:
        print(f"❌ demand_forecaster failed: {e}")
        return None
    
    try:
        from inventory_agent import IntelligentInventoryAgent
        components['inventory_agent'] = IntelligentInventoryAgent
        print("✅ inventory_agent loaded")
    except Exception as e:
        print(f"❌ inventory_agent failed: {e}")
        return None
    
    try:
        from visualization_dashboard import VisualizationDashboard
        components['visualization_dashboard'] = VisualizationDashboard
        print("✅ visualization_dashboard loaded")
    except Exception as e:
        print(f"❌ visualization_dashboard failed: {e}")
        return None
    
    return components

def run_simple_system():
    """Run the system with error handling"""
    
    print("🚀 INTELLIGENT INVENTORY MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # Safe import
    components = safe_import()
    if not components:
        print("❌ Failed to import all components. Check individual files.")
        return None
    
    print("\n📊 Initializing system components...")
    
    try:
        # Initialize components
        pattern_extractor = components['pattern_extractor']()
        
        # Extract patterns
        print("🔍 Extracting patterns...")
        real_data = pattern_extractor.load_walmart_kaggle_data()
        patterns = pattern_extractor.extract_patterns(real_data)
        
        # Generate synthetic data
        print("🎯 Generating demo data...")
        generator = components['synthetic_generator'](patterns)
        demo_data = generator.generate_demo_scenarios('Electronics', '2024-01-01', 180)
        
        # Setup forecaster
        print("🔮 Setting up forecaster...")
        forecaster = components['demand_forecaster']()
        prophet_data = demo_data[['Date', 'Sales']].rename(columns={'Date': 'ds', 'Sales': 'y'})
        train_data = prophet_data[:120]
        
        forecaster.build_model()
        forecaster.train(train_data)
        forecast = forecaster.forecast(periods=len(demo_data))
        
        # Initialize agent
        print("🤖 Initializing intelligent agent...")
        agent = components['inventory_agent'](initial_stock=3000, base_reorder_point=400)
        
        # Run simulation
        print("🎯 Running simulation...")
        simulation_results = []
        
        for idx, row in demo_data.iterrows():
            date = row['Date']
            scenario = row['Scenario_Name']
            forecast_value = max(0, forecast.iloc[idx]['yhat']) if idx < len(forecast) else 0
            
            decision = agent.make_intelligent_decision(forecast_value, date, scenario)
            simulation_results.append(decision)
            
            if decision['action'] != 'no_action':
                print(f"📅 {date.strftime('%Y-%m-%d')}: {decision['urgency_level']} - {decision['reason']}")
        
        # Show results
        print(f"\n📊 SIMULATION COMPLETE!")
        metrics = agent.get_performance_metrics()
        
        print(f"📈 Service Level: {metrics['operational']['service_level_percent']}%")
        print(f"💰 Profit: ${metrics['financial']['profit']:,.2f}")
        print(f"🎯 Orders Placed: {metrics['inventory']['total_orders_placed']}")
        print(f"🤖 Intelligent Decisions: {metrics['intelligence']['adaptive_decisions']}")
        
        # Create basic visualization
        try:
            dashboard = components['visualization_dashboard']()
            dashboard.create_comprehensive_dashboard(demo_data, simulation_results, agent.orders_placed)
            print("✅ Visualizations created!")
        except Exception as e:
            print(f"⚠️ Visualization error (non-critical): {e}")
        
        print("\n🎉 SYSTEM RUN SUCCESSFUL!")
        return demo_data, simulation_results, agent
        
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = run_simple_system()
    if result:
        print("🎯 Ready for capstone presentation!")
    else:
        print("🔧 Please check individual module files for errors.")