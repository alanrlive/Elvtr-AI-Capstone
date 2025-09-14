# working_demo.py
# Final working demo based on successful debug

import subprocess
import sys
import time
import requests
import os
from threading import Thread

def start_agent_service():
    """Start agent service with visible output"""
    
    print("🤖 Starting Agent Service...")
    
    services_dir = os.path.join(os.path.dirname(__file__), 'services')
    agent_script = os.path.join(services_dir, 'agent_service.py')
    
    # Start with visible output - we know this works!
    process = subprocess.Popen([
        sys.executable, agent_script
    ], cwd=services_dir)
    
    return process

def start_dashboard():
    """Start dashboard service"""
    
    print("📊 Starting Dashboard...")
    
    services_dir = os.path.join(os.path.dirname(__file__), 'services')
    dashboard_script = os.path.join(services_dir, 'dashboard_app.py')
    
    process = subprocess.Popen([
        sys.executable, dashboard_script
    ], cwd=services_dir)
    
    return process

def wait_for_service(url, name, timeout=15):
    """Wait for service to be ready"""
    
    print(f"⏳ Waiting for {name}...")
    
    for i in range(timeout):
        try:
            response = requests.get(f"{url}/api/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ {name} is ready!")
                return True
        except:
            pass
        
        time.sleep(1)
    
    print(f"⚠️ {name} taking longer than expected")
    return False

def run_data_generator():
    """Run the data generator"""
    
    print("\n📈 Starting Data Generator...")
    print("🎪 Demo scenarios will include:")
    print("   • Competitor stockout events")
    print("   • Viral social media spikes") 
    print("   • Celebrity endorsements")
    print("   • Supply chain disruptions")
    
    # Add required paths
    services_dir = os.path.join(os.path.dirname(__file__), 'services')
    core_modules_dir = os.path.join(os.path.dirname(__file__), '..', 'core_modules')
    
    sys.path.insert(0, services_dir)
    sys.path.insert(0, os.path.abspath(core_modules_dir))
    
    try:
        from data_generator import StreamingDataGenerator
        
        generator = StreamingDataGenerator()
        print("\n🚀 Starting 20-day demo (2 seconds per day)...")
        print("📊 Watch the dashboard at: http://localhost:5002")
        
        generator.run_quick_demo(demo_days=20)
        
    except Exception as e:
        print(f"❌ Data generator error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run the complete working demo"""
    
    print("🎉 WORKING INVENTORY AGENT DEMO")
    print("=" * 50)
    print("🎯 Based on successful debug results!")
    
    processes = []
    
    try:
        # Start Agent Service
        agent_process = start_agent_service()
        processes.append(('Agent Service', agent_process))
        
        # Give it a moment
        time.sleep(3)
        
        # Start Dashboard  
        dashboard_process = start_dashboard()
        processes.append(('Dashboard', dashboard_process))
        
        # Wait for services to be ready
        agent_ready = wait_for_service('http://localhost:5001', 'Agent Service')
        dashboard_ready = wait_for_service('http://localhost:5002', 'Dashboard', timeout=10)
        
        if not agent_ready:
            print("❌ Agent service not ready - but let's try anyway...")
        
        print(f"\n🎉 SERVICES RUNNING!")
        print("=" * 30)
        print("🤖 Agent Service: http://localhost:5001/api/health")
        print("📊 Live Dashboard: http://localhost:5002")
        
        print(f"\n📋 NEXT STEPS:")
        print("1. Open browser to: http://localhost:5002")
        print("2. Press Enter here to start the demo")
        print("3. Watch live agent decisions!")
        
        # Wait for user
        input("\n🎯 Press Enter when you're ready to start the demo...")
        
        # Run the data generator
        run_data_generator()
        
        print(f"\n🎉 Demo completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        print(f"\n🧹 Cleaning up...")
        for name, process in processes:
            try:
                process.terminate()
                print(f"✅ Stopped {name}")
            except:
                print(f"⚠️ {name} already stopped")
        
        print("✅ Cleanup complete!")

if __name__ == '__main__':
    main()