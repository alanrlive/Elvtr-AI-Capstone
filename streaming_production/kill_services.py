# kill_services.py
# Emergency script to stop all inventory system services

import subprocess
import sys
import time

def kill_python_processes():
    """Kill all Python processes (nuclear option)"""
    try:
        result = subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Killed all Python processes")
        else:
            print("⚠️ No Python processes found or already stopped")
    except Exception as e:
        print(f"❌ Error killing Python processes: {e}")

def kill_port_processes():
    """Kill processes running on our specific ports"""
    ports = [5001, 5002]
    
    for port in ports:
        try:
            # Find process using the port
            result = subprocess.run(['netstat', '-ano'], 
                                  capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) > 4:
                        pid = parts[-1]
                        print(f"🎯 Found process {pid} on port {port}")
                        
                        # Kill the process
                        kill_result = subprocess.run(['taskkill', '/F', '/PID', pid],
                                                   capture_output=True, text=True)
                        if kill_result.returncode == 0:
                            print(f"✅ Killed process {pid} on port {port}")
                        else:
                            print(f"⚠️ Could not kill process {pid}")
                            
        except Exception as e:
            print(f"❌ Error checking port {port}: {e}")

def main():
    print("🛑 EMERGENCY STOP - Inventory System Services")
    print("=" * 50)
    
    print("🔍 Checking for services to stop...")
    
    # Try specific port cleanup first
    kill_port_processes()
    
    print("\n💣 Nuclear option - killing all Python processes...")
    choice = input("Kill ALL Python processes? (y/N): ").strip().lower()
    
    if choice == 'y':
        kill_python_processes()
        print("🧹 All Python processes terminated")
    else:
        print("⏭️ Skipped nuclear option")
    
    # Verify ports are free
    time.sleep(2)
    print("\n🔍 Checking if ports are free...")
    
    try:
        result = subprocess.run(['netstat', '-ano'], 
                              capture_output=True, text=True)
        
        port_usage = {5001: False, 5002: False}
        
        for line in result.stdout.split('\n'):
            if ':5001' in line and 'LISTENING' in line:
                port_usage[5001] = True
            if ':5002' in line and 'LISTENING' in line:
                port_usage[5002] = True
        
        for port, in_use in port_usage.items():
            if in_use:
                print(f"⚠️ Port {port} still in use")
            else:
                print(f"✅ Port {port} is free")
                
    except Exception as e:
        print(f"❌ Could not check port status: {e}")
    
    print("\n🎉 Emergency stop complete!")
    print("💡 You can now restart the system safely")

if __name__ == '__main__':
    main()