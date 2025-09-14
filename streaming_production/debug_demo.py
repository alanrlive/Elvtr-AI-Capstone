# debug_demo.py
# Debug version to see what's going wrong

import subprocess
import sys
import time
import requests
import os

def debug_agent_service():
    """Start agent service and show any errors"""
    
    print("🔍 DEBUGGING AGENT SERVICE")
    print("=" * 40)
    
    services_dir = os.path.join(os.path.dirname(__file__), 'services')
    agent_script = os.path.join(services_dir, 'agent_service.py')
    
    print(f"📁 Services directory: {services_dir}")
    print(f"📄 Agent script: {agent_script}")
    print(f"📂 Script exists: {os.path.exists(agent_script)}")
    
    # Check if we can import the required modules
    print("\n🔍 Testing imports...")
    
    try:
        # Add paths
        sys.path.append(services_dir)
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core_modules'))
        
        print("✅ Paths added successfully")
        
        # Test core module imports
        try:
            from inventory_agent import IntelligentInventoryAgent
            print("✅ IntelligentInventoryAgent imported")
        except Exception as e:
            print(f"❌ IntelligentInventoryAgent import failed: {e}")
            return
        
        try:
            from demand_forecaster import DemandForecaster
            print("✅ DemandForecaster imported")
        except Exception as e:
            print(f"❌ DemandForecaster import failed: {e}")
            return
        
        # Test Flask imports
        try:
            from flask import Flask
            from flask_cors import CORS
            print("✅ Flask imports successful")
        except Exception as e:
            print(f"❌ Flask import failed: {e}")
            return
        
        print("\n🚀 All imports successful! Starting service with visible output...")
        
        # Start with visible output
        process = subprocess.Popen([
            sys.executable, agent_script
        ], cwd=services_dir)
        
        return process
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return None

def debug_paths():
    """Debug path issues"""
    
    print("🔍 DEBUGGING PATHS")
    print("=" * 30)
    
    current_dir = os.path.dirname(__file__)
    services_dir = os.path.join(current_dir, 'services')
    core_modules_dir = os.path.join(current_dir, '..', 'core_modules')
    
    print(f"📁 Current directory: {current_dir}")
    print(f"📁 Services directory: {services_dir}")
    print(f"📁 Core modules directory: {core_modules_dir}")
    
    print(f"\n📂 Services dir exists: {os.path.exists(services_dir)}")
    print(f"📂 Core modules dir exists: {os.path.exists(core_modules_dir)}")
    
    if os.path.exists(services_dir):
        print(f"\n📄 Files in services/:")
        for file in os.listdir(services_dir):
            print(f"   - {file}")
    
    if os.path.exists(core_modules_dir):
        print(f"\n📄 Files in core_modules/:")
        for file in os.listdir(core_modules_dir):
            print(f"   - {file}")
    
    # Test direct import
    print(f"\n🔍 Testing direct import from core_modules...")
    
    try:
        sys.path.insert(0, os.path.abspath(core_modules_dir))
        import inventory_agent
        print("✅ Direct import successful!")
        
        # Test class creation
        agent = inventory_agent.IntelligentInventoryAgent()
        print("✅ Agent creation successful!")
        
    except Exception as e:
        print(f"❌ Direct import failed: {e}")
        import traceback
        traceback.print_exc()

def run_minimal_test():
    """Run a minimal test without services"""
    
    print("\n🧪 RUNNING MINIMAL TEST")
    print("=" * 30)
    
    try:
        # Add core modules to path
        core_modules_dir = os.path.join(os.path.dirname(__file__), '..', 'core_modules')
        sys.path.insert(0, os.path.abspath(core_modules_dir))
        
        # Import and test agent
        from inventory_agent import IntelligentInventoryAgent
        
        agent = IntelligentInventoryAgent(initial_stock=1000)
        print("✅ Agent created successfully!")
        
        # Test a simple decision
        from datetime import datetime
        decision = agent.make_intelligent_decision(
            predicted_demand=100,
            current_date=datetime.now(),
            scenario_name="Normal_Operations"
        )
        
        print(f"✅ Agent decision: {decision['action']}")
        print(f"📦 Current stock: {decision['current_stock_after']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Minimal test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    
    print("🔍 DEBUGGING INVENTORY SYSTEM")
    print("=" * 50)
    
    # Check paths first
    debug_paths()
    
    # Run minimal test
    if run_minimal_test():
        print("\n🎯 Core system works! Let's debug the service...")
        
        # Try to start agent service with debug info
        process = debug_agent_service()
        
        if process:
            print("\n⏱️ Waiting 10 seconds to see if service starts...")
            time.sleep(10)
            
            # Check if it's working
            try:
                response = requests.get('http://localhost:5001/api/health', timeout=5)
                if response.status_code == 200:
                    print("🎉 SUCCESS! Agent service is running!")
                    print("📊 Try opening: http://localhost:5001/api/health")
                else:
                    print(f"⚠️ Service responding but with status: {response.status_code}")
            except Exception as e:
                print(f"❌ Service not responding: {e}")
            
            # Clean up
            try:
                process.terminate()
                print("🧹 Process terminated")
            except:
                pass
    
    else:
        print("\n❌ Core system has issues - need to fix imports first")

if __name__ == '__main__':
    main()