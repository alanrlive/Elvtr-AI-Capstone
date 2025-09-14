# test_imports.py
# Quick test to check all our module imports

print("🔍 Testing all module imports...")

try:
    from pattern_extractor import RealPatternExtractor
    print("✅ pattern_extractor imported successfully")
except ImportError as e:
    print(f"❌ pattern_extractor failed: {e}")

try:
    from synthetic_generator import EnhancedSyntheticGenerator
    print("✅ synthetic_generator imported successfully")
except ImportError as e:
    print(f"❌ synthetic_generator failed: {e}")

try:
    from demand_forecaster import DemandForecaster
    print("✅ demand_forecaster imported successfully")
except ImportError as e:
    print(f"❌ demand_forecaster failed: {e}")

try:
    from inventory_agent import IntelligentInventoryAgent
    print("✅ inventory_agent imported successfully")
except ImportError as e:
    print(f"❌ inventory_agent failed: {e}")

try:
    from visualization_dashboard import VisualizationDashboard
    print("✅ visualization_dashboard imported successfully")
except ImportError as e:
    print(f"❌ visualization_dashboard failed: {e}")

print("\n🎯 Import test complete!")

# Test basic functionality
try:
    print("\n🔧 Testing basic class instantiation...")
    extractor = RealPatternExtractor()
    print("✅ RealPatternExtractor created")
    
    forecaster = DemandForecaster()
    print("✅ DemandForecaster created")
    
    agent = IntelligentInventoryAgent()
    print("✅ IntelligentInventoryAgent created")
    
    dashboard = VisualizationDashboard()
    print("✅ VisualizationDashboard created")
    
    print("\n🎉 All components working!")
    
except Exception as e:
    print(f"❌ Component creation failed: {e}")