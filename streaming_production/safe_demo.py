# safe_demo.py
# VSCode-safe demo runner that won't kill windows

import subprocess
import sys
import time
import requests
import os
from threading import Thread

def start_agent_service_safe():
    """Start agent service without window interference"""
    
    print("🤖 Starting Agent Service...")
    
    try:
        services_dir = os.path.join(os.path.dirname(__file__), 'services')
        agent_script = os.path.join(services_dir, 'agent_service.py')
        
        # Start with minimal output to avoid window issues
        process = subprocess.Popen([
            sys.executable, agent_script
        ], cwd=services_dir, 
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE,
           creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start agent service: {e}")
        return None

def start_dashboard_safe():
    """Start dashboard service safely"""
    
    print("📊 Starting Dashboard...")
    
    try:
        services_dir = os.path.join(os.path.dirname(__file__), 'services')
        dashboard_script = os.path.join(services_dir, 'dashboard_app.py')
        
        process = subprocess.Popen([
            sys.executable, dashboard_script
        ], cwd=services_dir,
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE,
           creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        return None

def check_service_health_safe(url, service_name, timeout=20):
    """Check service health without blocking"""
    
    print(f"🔍 Checking {service_name}...")
    
    for i in range(timeout):
        try:
            response = requests.get(f"{url}/api/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ {service_name} is healthy!")
                return True
        except:
            pass
        
        print(f"   Waiting... ({i+1}/{timeout})")
        time.sleep(1)
    
    print(f"❌ {service_name} failed to start")
    return False

def run_data_generator_safe():
    """Run data generator in a controlled way"""
    
    print("📈 Starting Data Generator...")
    
    # Import and run directly instead of subprocess
    sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core_modules'))
    
    try:
        from data_generator import StreamingDataGenerator
        
        generator = StreamingDataGenerator()
        
        print("🎪 Running demo with these scenarios:")
        print("   • Day 3: Competitor stockout")
        print("   • Day 8: Viral social media event")
        print("   • Day 15: Celebrity endorsement")
        
        # Run for limited time to avoid infinite loop
        generator.run_quick_demo(demo_days=20)
        
    except Exception as e:
        print(f"❌ Data generator error: {e}")

def safe_cleanup(processes):
    """Safely clean up processes"""
    
    print("\n🧹 Cleaning up...")
    
    for name, process in processes:
        try:
            process.terminate()
            time.sleep(1)
            if process.poll() is None:
                process.kill()
            print(f"✅ Stopped {name}")
        except:
            print(f"⚠️ {name} already stopped")

def run_safe_demo():
    """Run a completely safe demo"""
    
    print("🎪 VSCODE-SAFE DEMO MODE")
    print("=" * 40)
    print("🛡️ No window interference")
    print("📊 Dashboard: http://localhost:5002")
    print("🤖 Agent API: http://localhost:5001")
    
    processes = []
    
    try:
        # Start services
        agent_process = start_agent_service_safe()
        if agent_process:
            processes.append(('Agent Service', agent_process))
            
        dashboard_process = start_dashboard_safe()
        if dashboard_process:
            processes.append(('Dashboard', dashboard_process))
        
        # Give services time to start
        print("\n⏳ Waiting for services to initialize...")
        time.sleep(5)
        
        # Check health
        agent_healthy = check_service_health_safe('http://localhost:5001', 'Agent Service')
        dashboard_healthy = check_service_health_safe('http://localhost:5002', 'Dashboard')
        
        if not agent_healthy:
            print("❌ Cannot continue without agent service")
            safe_cleanup(processes)
            return
        
        print("\n🎉 SERVICES READY!")
        print("=" * 30)
        print("📊 Dashboard: http://localhost:5002")
        print("🤖 Agent API: http://localhost:5001/api/health")
        print("\n💡 MANUAL STEPS:")
        print("1. Open browser to: http://localhost:5002")
        print("2. Press Enter here to start data stream")
        print("3. Watch the live dashboard!")
        
        # Wait for user to open dashboard
        input("\n👆 Press Enter when dashboard is open...")
        
        # Run data generator
        print("\n🚀 Starting demo data stream...")
        run_data_generator_safe()
        
        print("\n🎉 Demo completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    finally:
        safe_cleanup(processes)
        print("✅ Cleanup complete")

def check_ports():
    """Check if ports are free"""
    
    print("🔍 Checking ports...")
    
    ports_free = True
    
    for port in [5001, 5002]:
        try:
            response = requests.get(f'http://localhost:{port}/api/health', timeout=2)
            print(f"⚠️ Port {port} is already in use")
            ports_free = False
        except:
            print(f"✅ Port {port} is free")
    
    return ports_free

def main():
    """Main safe demo function"""
    
    print("🛡️ VSCODE-SAFE INVENTORY DEMO")
    print("=" * 40)
    
    # Check if ports are free
    if not check_ports():
        print("\n💡 Some ports are in use. Clean up first?")
        choice = input("Run cleanup? (y/N): ").strip().lower()
        
        if choice == 'y':
            import kill_services
            kill_services.main()
            time.sleep(2)
    
    print("\n🚀 Starting safe demo...")
    run_safe_demo()

if __name__ == '__main__':
    main()