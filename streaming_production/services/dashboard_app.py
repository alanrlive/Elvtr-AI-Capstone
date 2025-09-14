# simple_dashboard.py
# Template-free dashboard that serves HTML directly

from flask import Flask, jsonify, Response
from flask_cors import CORS
import requests
import json
import threading
import time

app = Flask(__name__)
CORS(app)

# Store latest data
latest_data = {
    'agent_metrics': {},
    'current_day': 0,
    'decisions': [],
    'last_update': 'Never'
}

def monitor_agent():
    """Monitor agent service in background"""
    while True:
        try:
            # Get current state
            response = requests.get('http://localhost:5001/api/current-state', timeout=2)
            if response.status_code == 200:
                state = response.json()
                
                # Get performance metrics
                perf_response = requests.get('http://localhost:5001/api/performance-summary', timeout=2)
                if perf_response.status_code == 200:
                    perf_data = perf_response.json()
                    
                    # Update latest data
                    latest_data['agent_metrics'] = perf_data.get('service_metrics', {})
                    latest_data['current_day'] = state.get('current_day', 0)
                    latest_data['decisions'] = state.get('recent_decisions', [])
                    latest_data['last_update'] = time.strftime('%H:%M:%S')
                    
        except Exception as e:
            print(f"Monitor error: {e}")
        
        time.sleep(2)

# Start monitoring in background
monitor_thread = threading.Thread(target=monitor_agent, daemon=True)
monitor_thread.start()

@app.route('/')
def dashboard():
    """Return simple HTML dashboard"""
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Intelligent Inventory Agent - Live Dashboard</title>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="5">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            margin: 20px;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .header {{
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-box {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #3498db;
        }}
        .metric-value {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            color: #7f8c8d;
            font-size: 0.9rem;
            margin-top: 5px;
        }}
        .decisions {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            max-height: 300px;
            overflow-y: auto;
        }}
        .decision {{
            background: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #3498db;
        }}
        .status {{
            background: #27ae60;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .profit {{ color: #27ae60; }}
        .service-level {{ color: #3498db; }}
        .orders {{ color: #e67e22; }}
        .current-day {{ color: #9b59b6; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Intelligent Inventory Agent</h1>
            <p>Real-time Production Dashboard</p>
        </div>
        
        <div class="status">
            🟢 Live System Running - Last Update: {latest_data['last_update']} - Auto-refresh every 5 seconds
        </div>
        
        <div class="metrics">
            <div class="metric-box">
                <div class="metric-value current-day">{latest_data['current_day']}</div>
                <div class="metric-label">Current Day</div>
            </div>
            
            <div class="metric-box">
                <div class="metric-value profit">${latest_data['agent_metrics'].get('total_revenue', 0) - latest_data['agent_metrics'].get('total_costs', 0):,.0f}</div>
                <div class="metric-label">Total Profit</div>
            </div>
            
            <div class="metric-box">
                <div class="metric-value service-level">{latest_data['agent_metrics'].get('service_level', 100):.1f}%</div>
                <div class="metric-label">Service Level</div>
            </div>
            
            <div class="metric-box">
                <div class="metric-value orders">{latest_data['agent_metrics'].get('orders_placed', 0)}</div>
                <div class="metric-label">Orders Placed</div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <h3>📋 Recent Agent Decisions</h3>
        <div class="decisions">
"""
    
    # Add recent decisions
    if latest_data['decisions']:
        for i, decision_entry in enumerate(latest_data['decisions'][-10:]):
            decision = decision_entry.get('decision', {})
            date = decision.get('date', 'Unknown')
            action = decision.get('action', 'no_action')
            stock = decision.get('current_stock_after', 0)
            scenario = decision.get('scenario', 'Unknown')
    
            # Calculate the actual day number for this decision
            actual_day = max(1, latest_data['current_day'] - len(latest_data['decisions']) + i + 1)
            print(f"Current day: {latest_data['current_day']}, Decisions count: {len(latest_data['decisions'])}, Calculated day for entry {i}: {actual_day}")
            
            html += f"""
            <div class="decision">
                <strong>Day {actual_day} - {date}</strong><br>
                Action: {action}<br>
                Stock Level: {stock:.0f} units<br>
                Scenario: {scenario.replace('_', ' ')}
            </div>
"""
    else:
        html += "<div class='decision'>Waiting for agent decisions...</div>"
    
    html += """
        </div>
    </div>
    
    <div class="container">
        <h3>📊 API Endpoints</h3>
        <p><a href="/api/data" target="_blank">📊 Current Data (JSON)</a></p>
        <p><a href="http://localhost:5001/api/health" target="_blank">🤖 Agent Health Check</a></p>
        <p><a href="http://localhost:5001/api/current-state" target="_blank">📈 Agent Current State</a></p>
    </div>
</body>
</html>
"""
    
    return Response(html, mimetype='text/html')

@app.route('/api/data')
def get_data():
    """Return current data as JSON"""
    return jsonify(latest_data)

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Simple Dashboard',
        'agent_connected': latest_data['current_day'] > 0
    })

if __name__ == '__main__':
    print("📊 Starting Simple Dashboard...")
    print("🌐 Dashboard: http://localhost:5002")
    print("📱 Auto-refresh every 5 seconds")
    print("🔄 Monitoring agent at http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5002, debug=False)