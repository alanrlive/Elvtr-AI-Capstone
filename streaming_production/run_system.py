# streaming_production/run_system.py
# Easy startup script for the complete production system

import subprocess
import sys
import time
import requests
import os
from multiprocessing import Process

def check_dependencies():
    """Check if required packages are installed"""
    
    required_packages = [
        'flask', 'flask-cors', 'flask-socketio', 'requests', 
        'pandas', 'numpy', 'prophet', 'plotly'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print(f"💡 Install with: pip install {' '.join(missing)}")
        return False
    
    return True

def check_service_health(url, service_name, timeout=30):
    """Check if a service is healthy"""
    
    print(f"🔍 Checking {service_name}...")
    
    for i in range(timeout):
        try:
            response = requests.get(f"{url}/api/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ {service_name} is healthy!")
                return True
        except:
            pass
        
        time.sleep(1)
    
    print(f"❌ {service_name} failed to start")
    return False

def start_agent_service():
    """Start the agent service"""
    
    print("🚀 Starting Agent Service...")
    
    try:
        # Change to services directory
        services_dir = os.path.join(os.path.dirname(__file__), 'services')
        agent_script = os.path.join(services_dir, 'agent_service.py')
        
        # Start agent service
        process = subprocess.Popen([
            sys.executable, agent_script
        ], cwd=services_dir)
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start agent service: {e}")
        return None

def start_dashboard():
    """Start the dashboard"""
    
    print("📊 Starting Live Dashboard...")
    
    try:
        # Change to services directory  
        services_dir = os.path.join(os.path.dirname(__file__), 'services')
        dashboard_script = os.path.join(services_dir, 'dashboard_app.py')
        
        # Start dashboard
        process = subprocess.Popen([
            sys.executable, dashboard_script
        ], cwd=services_dir)
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        return None

def start_data_generator():
    """Start the data generator"""
    
    print("📈 Starting Data Generator...")
    
    try:
        services_dir = os.path.join(os.path.dirname(__file__), 'services')
        generator_script = os.path.join(services_dir, 'data_generator.py')
        
        # Start data generator
        process = subprocess.Popen([
            sys.executable, generator_script
        ], cwd=services_dir)
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start data generator: {e}")
        return None

def run_production_system():
    """Run the complete production system"""
    
    print("🚀 INTELLIGENT INVENTORY AGENT - PRODUCTION SYSTEM")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 Install missing packages and try again")
        return
    
    print("✅ All dependencies available")
    
    # Create templates directory if it doesn't exist
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(template_dir, exist_ok=True)
    
    # Create the dashboard.html file in templates directory
    dashboard_html_path = os.path.join(template_dir, 'dashboard.html')
    if not os.path.exists(dashboard_html_path):
        print("📝 Creating dashboard template...")
        # You'll need to copy the dashboard.html content here
        print("⚠️  Please ensure dashboard.html is in the templates/ directory")
    
    processes = []
    
    try:
        # Start Agent Service
        agent_process = start_agent_service()
        if agent_process:
            processes.append(('Agent Service', agent_process))
            time.sleep(3)  # Give it time to start
        
        # Check if agent service is running
        if not check_service_health('http://localhost:5001', 'Agent Service'):
            print("❌ Cannot continue without agent service")
            return
        
        # Start Dashboard
        dashboard_process = start_dashboard()
        if dashboard_process:
            processes.append(('Dashboard', dashboard_process))
            time.sleep(3)  # Give it time to start
        
        # Check if dashboard is running
        if not check_service_health('http://localhost:5002', 'Dashboard'):
            print("⚠️  Dashboard may not be fully ready, but continuing...")
        
        print("\n🎉 SYSTEM READY!")
        print("=" * 60)
        print("🤖 Agent Service: http://localhost:5001")
        print("📊 Live Dashboard: http://localhost:5002")
        print("📈 Data Generator: Ready to start")
        print("\n📋 NEXT STEPS:")
        print("1. Open dashboard: http://localhost:5002")
        print("2. Start data generator manually, or...")
        print("3. Choose option below:")
        
        # Ask user what to do next
        print("\n🎯 What would you like to do?")
        print("1. Start data generator (normal speed)")
        print("2. Start data generator (demo speed - 2 sec/day)")
        print("3. Just run services (manual control)")
        print("4. Exit")
        
        choice = input("\nChoice (1-4): ").strip()
        
        if choice == '1':
            print("\n🎯 Starting data generator (normal speed)...")
            generator_process = start_data_generator()
            if generator_process:
                processes.append(('Data Generator', generator_process))
        
        elif choice == '2':
            print("\n🎪 Starting demo mode data generator...")
            services_dir = os.path.join(os.path.dirname(__file__), 'services')
            generator_script = os.path.join(services_dir, 'data_generator.py')
            
            # Start with demo parameters
            generator_process = subprocess.Popen([
                sys.executable, '-c',
                f"""
import sys
sys.path.append('{services_dir}')
from data_generator import StreamingDataGenerator
generator = StreamingDataGenerator()
generator.run_quick_demo(demo_days=30)
"""
            ], cwd=services_dir)
            
            if generator_process:
                processes.append(('Demo Data Generator', generator_process))
        
        elif choice == '3':
            print("\n🎮 Services running - manual control mode")
            print("💡 You can now:")
            print("   • Open http://localhost:5002 for dashboard")
            print("   • Manually run data_generator.py")
            print("   • Use the agent API directly")
        
        elif choice == '4':
            print("\n👋 Exiting...")
            cleanup_processes(processes)
            return
        
        # Keep system running
        print(f"\n🔄 System running with {len(processes)} processes...")
        print("⏹️  Press Ctrl+C to stop all services")
        
        try:
            while True:
                # Check if processes are still running
                active_processes = []
                for name, process in processes:
                    if process.poll() is None:  # Still running
                        active_processes.append((name, process))
                    else:
                        print(f"⚠️  {name} stopped unexpectedly")
                
                processes = active_processes
                
                if not processes:
                    print("❌ All processes stopped")
                    break
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            print(f"\n⏹️  Stopping system...")
            cleanup_processes(processes)
            
    except Exception as e:
        print(f"❌ System error: {e}")
        cleanup_processes(processes)

def cleanup_processes(processes):
    """Clean up all running processes"""
    
    print("🧹 Cleaning up processes...")
    
    for name, process in processes:
        try:
            print(f"   Stopping {name}...")
            process.terminate()
            
            # Wait for graceful shutdown
            try:
                process.wait(timeout=3)
                print(f"   ✅ {name} stopped gracefully")
            except subprocess.TimeoutExpired:
                print(f"   🔥 Force killing {name}...")
                process.kill()
                process.wait(timeout=2)
                print(f"   ✅ {name} force stopped")
                
        except Exception as e:
            print(f"   ⚠️ Error stopping {name}: {e}")
            # Try to force kill anyway
            try:
                process.kill()
            except:
                pass
    
    # Also try to kill any remaining processes on our ports
    try:
        import subprocess
        # Kill anything on port 5001 and 5002
        subprocess.run(['taskkill', '/F', '/FI', 'MEMUSAGE gt 1'], 
                      capture_output=True, shell=True)
        print("🧹 Cleaned up any remaining processes")
    except:
        pass
    
    print("✅ Cleanup complete")

def run_quick_demo():
    """Run a quick demo version"""
    
    print("🎪 QUICK DEMO MODE")
    print("=" * 30)
    print("⚡ Fast demo with key scenarios")
    print("📊 Dashboard updates every 2 seconds")
    print("🎯 Perfect for presentations!")
    
    # Check dependencies
    if not check_dependencies():
        return
    
    processes = []
    
    try:
        # Start agent service
        agent_process = start_agent_service()
        if agent_process:
            processes.append(('Agent Service', agent_process))
            time.sleep(2)
        
        # Start dashboard
        dashboard_process = start_dashboard()
        if dashboard_process:
            processes.append(('Dashboard', dashboard_process))
            time.sleep(2)
        
        # Verify services
        if not check_service_health('http://localhost:5001', 'Agent Service', timeout=10):
            print("❌ Agent service not ready")
            return
        
        print("\n🎉 DEMO READY!")
        print("📊 Dashboard: http://localhost:5002")
        print("⚡ Auto-starting demo data stream...")
        
        # Start demo data generator
        services_dir = os.path.join(os.path.dirname(__file__), 'services')
        demo_cmd = f"""
import sys, os
sys.path.append('{services_dir}')
sys.path.append(os.path.join('{os.path.dirname(__file__)}', '..', 'core_modules'))
from data_generator import StreamingDataGenerator
generator = StreamingDataGenerator()
generator.run_quick_demo(demo_days=25)
"""
        
        generator_process = subprocess.Popen([
            sys.executable, '-c', demo_cmd
        ], cwd=services_dir)
        
        if generator_process:
            processes.append(('Demo Generator', generator_process))
        
        print("🎯 Demo running! Watch the dashboard for live updates...")
        print("⏹️  Press Ctrl+C to stop")
        
        # Wait for demo to complete or user interrupt
        try:
            generator_process.wait()
            print("\n🎉 Demo completed!")
        except KeyboardInterrupt:
            print(f"\n⏹️  Demo stopped by user")
        
        cleanup_processes(processes)
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        cleanup_processes(processes)

def check_system_requirements():
    """Check system requirements and provide setup guidance"""
    
    print("🔍 SYSTEM REQUIREMENTS CHECK")
    print("=" * 40)
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor} (need 3.8+)")
        return False
    
    # Check required packages
    print("📦 Checking packages...")
    if check_dependencies():
        print("✅ All required packages installed")
    else:
        print("❌ Missing packages - install with pip")
        return False
    
    # Check file structure
    print("📁 Checking file structure...")
    required_dirs = ['services', 'templates']
    current_dir = os.path.dirname(__file__)
    
    for dir_name in required_dirs:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"✅ {dir_name}/ directory")
        else:
            print(f"❌ {dir_name}/ directory missing")
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Created {dir_name}/ directory")
    
    # Check core modules
    core_modules_dir = os.path.join(current_dir, '..', 'core_modules')
    if os.path.exists(core_modules_dir):
        print("✅ Core modules directory")
    else:
        print("❌ Core modules directory missing")
        print("💡 Make sure your core_modules/ folder is in the parent directory")
        return False
    
    print("\n🎯 System ready for production!")
    return True

def main():
    """Main function with menu"""
    
    print("🚀 INTELLIGENT INVENTORY AGENT")
    print("Production Streaming System")
    print("=" * 50)
    
    print("\nChoose an option:")
    print("1. 🔍 Check system requirements")
    print("2. 🚀 Run full production system")
    print("3. 🎪 Run quick demo (presentation mode)")
    print("4. 📋 Show system information")
    print("5. 🧹 Cleanup and exit")
    
    choice = input("\nChoice (1-5): ").strip()
    
    if choice == '1':
        check_system_requirements()
        
    elif choice == '2':
        if check_system_requirements():
            run_production_system()
        else:
            print("❌ System requirements not met")
            
    elif choice == '3':
        if check_system_requirements():
            run_quick_demo()
        else:
            print("❌ System requirements not met")
            
    elif choice == '4':
        print("\n📋 SYSTEM INFORMATION")
        print("=" * 30)
        print("🤖 Agent Service: http://localhost:5001")
        print("📊 Dashboard: http://localhost:5002") 
        print("📈 Data Generator: Streams data every 10 seconds")
        print("🎯 Demo Mode: 2 seconds per day for presentations")
        print("\n📁 File Structure:")
        print("   streaming_production/")
        print("   ├── services/")
        print("   │   ├── agent_service.py")
        print("   │   ├── data_generator.py")
        print("   │   └── dashboard_app.py")
        print("   ├── templates/")
        print("   │   └── dashboard.html")
        print("   └── run_system.py")
        
    elif choice == '5':
        print("👋 Goodbye!")
        
    else:
        print("❌ Invalid choice")
        main()

if __name__ == '__main__':
    main()