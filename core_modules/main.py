# main.py
# Main integration file for the Intelligent Inventory Management System

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import our modular components
from pattern_extractor import RealPatternExtractor
from synthetic_generator import EnhancedSyntheticGenerator
from demand_forecaster import DemandForecaster
from inventory_agent import IntelligentInventoryAgent
from visualization_dashboard import VisualizationDashboard

class InventoryManagementSystem:
    """Complete Intelligent Inventory Management System"""
    
    def __init__(self):
        # Initialize all components
        self.pattern_extractor = RealPatternExtractor()
        self.synthetic_generator = None
        self.demand_forecaster = DemandForecaster()
        self.inventory_agent = IntelligentInventoryAgent()
        self.dashboard = VisualizationDashboard()
        
        # Data storage
        self.real_patterns = None
        self.demo_data = None
        self.simulation_results = []
        
        print("🚀 Intelligent Inventory Management System Initialized")
        
    def setup_system(self, kaggle_data_path=None, category='Electronics', simulation_days=180):
        """Setup the complete system with data and models"""
        
        print("\n📊 Setting up system components...")
        
        # Step 1: Extract real patterns
        print("🔍 Step 1: Extracting real market patterns...")
        real_data = self.pattern_extractor.load_walmart_kaggle_data(kaggle_data_path)
        self.real_patterns = self.pattern_extractor.extract_patterns(real_data)
        
        # Step 2: Initialize synthetic generator
        print("🎯 Step 2: Initializing demo scenario generator...")
        self.synthetic_generator = EnhancedSyntheticGenerator(self.real_patterns)
        
        # Step 3: Generate hybrid demo data
        print("📈 Step 3: Generating hybrid demo dataset...")
        self.demo_data = self.synthetic_generator.generate_demo_scenarios(
            category=category, 
            days=simulation_days
        )
        
        # Step 4: Setup demand forecaster
        print("🔮 Step 4: Training demand forecasting model...")
        prophet_data = self.demo_data[['Date', 'Sales']].rename(columns={'Date': 'ds', 'Sales': 'y'})
        train_size = int(len(prophet_data) * 0.8)
        train_data = prophet_data[:train_size]
        
        self.demand_forecaster.build_model()
        self.demand_forecaster.train(train_data)
        
        print("✅ System setup complete!")
        return self
    
    def run_simulation(self, agent_config=None):
        """Run the complete inventory simulation"""
        
        print("\n🎯 Running intelligent inventory simulation...")
        
        # Configure agent if needed
        if agent_config:
            self.inventory_agent = IntelligentInventoryAgent(**agent_config)
        
        # Reset simulation state
        self.simulation_results = []
        
        # Generate forecast for entire period
        forecast = self.demand_forecaster.forecast(periods=len(self.demo_data))
        
        # Run day-by-day simulation
        for idx, row in self.demo_data.iterrows():
            date = row['Date']
            actual_sales = row['Sales']
            scenario = row['Scenario_Name']
            
            # Get forecast for this date
            forecast_value = max(0, forecast.iloc[idx]['yhat']) if idx < len(forecast) else max(0, actual_sales)
            
            # Agent makes intelligent decision
            decision = self.inventory_agent.make_intelligent_decision(forecast_value, date, scenario)
            self.simulation_results.append(decision)
            
            # Log critical decisions
            if decision['action'] != 'no_action':
                print(f"📅 {date.strftime('%Y-%m-%d')}: {decision['urgency_level']} - {decision['reason']}")
        
        print(f"✅ Simulation complete! Processed {len(self.simulation_results)} days")
        return self.simulation_results
    
    def analyze_performance(self):
        """Analyze and display complete performance metrics"""
        
        print("\n📊 Analyzing system performance...")
        
        # Get comprehensive metrics
        performance_metrics = self.inventory_agent.get_performance_metrics()
        scenario_performance = self.inventory_agent.get_scenario_performance()
        
        # Display summary
        self.inventory_agent.print_performance_summary()
        
        return performance_metrics, scenario_performance
    
    def create_visualizations(self, save_plots=True):
        """Create comprehensive visualization dashboard"""
        
        print("\n📈 Creating visualization dashboard...")
        
        # Main comprehensive dashboard
        if save_plots:
            self.dashboard.create_comprehensive_dashboard(
                self.demo_data, 
                self.simulation_results, 
                self.inventory_agent.orders_placed,
                save_path='inventory_dashboard.png'
            )
        else:
            self.dashboard.create_comprehensive_dashboard(
                self.demo_data, 
                self.simulation_results, 
                self.inventory_agent.orders_placed
            )
        
        # Performance timeline
        if save_plots:
            self.dashboard.create_performance_timeline(
                self.simulation_results,
                save_path='performance_timeline.png'
            )
        else:
            self.dashboard.create_performance_timeline(self.simulation_results)
        
        # Scenario comparison
        scenario_performance = self.inventory_agent.get_scenario_performance()
        if save_plots:
            self.dashboard.create_scenario_comparison(
                scenario_performance,
                save_path='scenario_comparison.png'
            )
        else:
            self.dashboard.create_scenario_comparison(scenario_performance)
        
        print("✅ All visualizations created!")
    
    def export_results(self, export_path='simulation_results'):
        """Export all results for further analysis"""
        
        print(f"\n💾 Exporting results to {export_path}/...")
        
        import os
        os.makedirs(export_path, exist_ok=True)
        
        # Export simulation decisions
        self.inventory_agent.export_decisions_log(f'{export_path}/decisions_log.csv')
        
        # Export demo data
        self.demo_data.to_csv(f'{export_path}/demo_data.csv', index=False)
        
        # Export performance metrics
        metrics = self.inventory_agent.get_performance_metrics()
        scenario_perf = self.inventory_agent.get_scenario_performance()
        
        # Create summary report
        self._create_summary_report(metrics, scenario_perf, f'{export_path}/performance_report.txt')
        
        print("✅ All results exported!")
    
    def _create_summary_report(self, metrics, scenario_perf, filepath):
        """Create a detailed text report"""
        
        with open(filepath, 'w') as f:
            f.write("INTELLIGENT INVENTORY MANAGEMENT SYSTEM - PERFORMANCE REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Service Level Achieved: {metrics['operational']['service_level_percent']}%\n")
            f.write(f"Profit Generated: ${metrics['financial']['profit']:,.2f}\n")
            f.write(f"Stockout Prevention: {metrics['operational']['total_days_simulated'] - metrics['operational']['stockouts']} out of {metrics['operational']['total_days_simulated']} days\n")
            f.write(f"Intelligent Adaptations: {metrics['intelligence']['adaptive_decisions']} scenario-based decisions\n\n")
            
            # Detailed Metrics
            f.write("DETAILED PERFORMANCE METRICS\n")
            f.write("-" * 35 + "\n")
            
            for category, data in metrics.items():
                f.write(f"\n{category.upper()}:\n")
                for key, value in data.items():
                    f.write(f"  {key}: {value}\n")
            
            # Scenario Analysis
            f.write("\nSCENARIO PERFORMANCE ANALYSIS\n")
            f.write("-" * 35 + "\n")
            
            for scenario, perf in scenario_perf.items():
                f.write(f"\n{scenario}:\n")
                f.write(f"  Encounters: {perf['encounters']}\n")
                f.write(f"  Fulfillment Rate: {perf['fulfillment_rate']:.1f}%\n")
                f.write(f"  Average Demand: {perf['avg_demand']:.1f}\n")
                f.write(f"  Primary Strategy: {perf['most_common_urgency']}\n")
        
        print(f"✅ Summary report created: {filepath}")
    
    def get_demo_scenarios_info(self):
        """Get information about demo scenarios for presentation"""
        
        if self.synthetic_generator:
            return self.synthetic_generator.get_scenario_descriptions()
        else:
            return {}
    
    def quick_demo(self, days=90):
        """Run a quick demo for testing"""
        
        print("🚀 Running Quick Demo (90 days)...")
        
        # Quick setup
        self.setup_system(simulation_days=days)
        
        # Run simulation
        self.run_simulation()
        
        # Show results
        self.analyze_performance()
        
        # Create visualizations
        self.create_visualizations(save_plots=False)
        
        print("✅ Quick demo complete!")
        return self

def run_complete_system():
    """Main function to run the complete system"""
    
    print("🚀 INTELLIGENT INVENTORY MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # Initialize system
    system = InventoryManagementSystem()
    
    # Setup with full configuration
    system.setup_system(
        kaggle_data_path=None,  # Uses synthetic patterns
        category='Electronics',
        simulation_days=180
    )
    
    # Run simulation with custom agent configuration
    agent_config = {
        'initial_stock': 3000,
        'base_reorder_point': 400,
        'base_reorder_quantity': 1000
    }
    
    results = system.run_simulation(agent_config)
    
    # Analyze performance
    metrics, scenario_perf = system.analyze_performance()
    
    # Create visualizations
    system.create_visualizations(save_plots=True)
    
    # Export results
    system.export_results('capstone_results')
    
    # Print scenario information for presentation
    scenarios = system.get_demo_scenarios_info()
    print(f"\n🎯 DEMO SCENARIOS AVAILABLE FOR PRESENTATION:")
    for scenario, info in scenarios.items():
        print(f"   • {scenario}: {info['description']} ({info['period']})")
    
    print(f"\n🎉 COMPLETE SYSTEM ANALYSIS FINISHED!")
    print(f"📊 Check 'capstone_results/' folder for exported data")
    print(f"📈 Visualization files saved as PNG images")
    print(f"🎯 Your agent successfully handled {len(results)} days of operations!")
    
    return system

# Configuration options for different demo scenarios
DEMO_CONFIGS = {
    'quick_test': {
        'simulation_days': 30,
        'agent_config': {'initial_stock': 1500, 'base_reorder_point': 200}
    },
    'standard_demo': {
        'simulation_days': 180,
        'agent_config': {'initial_stock': 3000, 'base_reorder_point': 400}
    },
    'full_year': {
        'simulation_days': 365,
        'agent_config': {'initial_stock': 5000, 'base_reorder_point': 600}
    }
}

def run_custom_demo(config_name='standard_demo'):
    """Run system with predefined configurations"""
    
    config = DEMO_CONFIGS.get(config_name, DEMO_CONFIGS['standard_demo'])
    
    system = InventoryManagementSystem()
    system.setup_system(simulation_days=config['simulation_days'])
    system.run_simulation(config['agent_config'])
    system.analyze_performance()
    system.create_visualizations(save_plots=True)
    
    return system

if __name__ == "__main__":
    # Run the complete system
    system = run_complete_system()
    
    print("\n" + "="*60)
    print("🎉 SYSTEM READY FOR CAPSTONE PRESENTATION!")
    print("="*60)
    print("📁 All files organized in separate modules")
    print("📊 Comprehensive visualizations created") 
    print("📈 Performance metrics calculated")
    print("🤖 Intelligent agent successfully tested")
    print("🎯 Ready to demo advanced inventory management!")