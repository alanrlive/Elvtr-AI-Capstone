# streaming_production/services/agent_service.py
# Production Agent Microservice - REST API for intelligent inventory decisions

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import sys

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../core_modules'))

from inventory_agent import IntelligentInventoryAgent
from demand_forecaster import DemandForecaster

app = Flask(__name__)
CORS(app)

class ProductionAgentService:
    """Production-ready agent service with REST API"""
    
    def __init__(self):
        # Initialize core components
        self.agent = IntelligentInventoryAgent(
            initial_stock=3000,
            base_reorder_point=400,
            base_reorder_quantity=1000
        )
        
        # Service state
        self.current_day = 0
        self.service_start_time = datetime.now()
        self.total_decisions = 0
        self.system_status = "running"
        
        # Data storage
        self.daily_data_log = []
        self.decision_log = []
        self.performance_metrics = {
            "total_revenue": 0,
            "total_costs": 0,
            "stockouts": 0,
            "orders_placed": 0,
            "service_level": 100.0
        }
        
        print("🚀 Production Agent Service Initialized")
        print(f"⚡ Service started at: {self.service_start_time}")
        print(f"📦 Initial inventory: {self.agent.current_stock} units")
    
    def process_daily_data(self, daily_data):
        """Process incoming daily data and make intelligent decisions"""
        
        try:
            # Extract data
            date_str = daily_data.get('date')
            sales = float(daily_data.get('sales', 0))
            scenario = daily_data.get('scenario', 'Normal_Operations')
            predicted_demand = float(daily_data.get('predicted_demand', sales))
            
            # Convert date
            current_date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Agent makes intelligent decision
            decision = self.agent.make_intelligent_decision(
                predicted_demand=predicted_demand,
                current_date=current_date,
                scenario_name=scenario
            )
            
            # Update service metrics
            self.current_day += 1
            self.total_decisions += 1
            
            # Update performance tracking
            self._update_performance_metrics(decision, sales)
            
            # Log data and decision
            self.daily_data_log.append({
                'day': self.current_day,
                'date': date_str,
                'sales': sales,
                'scenario': scenario,
                'predicted_demand': predicted_demand,
                'timestamp': datetime.now().isoformat()
            })
            
            self.decision_log.append({
                'day': self.current_day,
                'decision': decision,
                'timestamp': datetime.now().isoformat()
            })
            
            # Generate response
            response = self._create_response(decision, sales, scenario)
            
            # Log significant decisions
            if decision['action'] != 'no_action':
                print(f"📅 Day {self.current_day}: {decision['urgency_level']} - {decision['reason']}")
            
            return response
            
        except Exception as e:
            print(f"❌ Error processing daily data: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _update_performance_metrics(self, decision, actual_sales):
        """Update real-time performance metrics"""
        
        # Revenue calculation (assume $50 per unit)
        revenue_per_unit = 50
        fulfilled_demand = min(actual_sales, decision['current_stock_before'])
        self.performance_metrics['total_revenue'] += fulfilled_demand * revenue_per_unit
        
        # Cost calculation (assume $30 per unit)
        if decision['action'] == 'intelligent_reorder':
            cost_per_unit = 30
            order_cost = decision['order_quantity'] * cost_per_unit
            self.performance_metrics['total_costs'] += order_cost
            self.performance_metrics['orders_placed'] += 1
        
        # Stockout tracking
        if decision['action'] == 'stockout':
            self.performance_metrics['stockouts'] += 1
        
        # Service level calculation
        if self.current_day > 0:
            self.performance_metrics['service_level'] = (
                (self.current_day - self.performance_metrics['stockouts']) / self.current_day * 100
            )
    
    def _create_response(self, decision, actual_sales, scenario):
        """Create comprehensive API response"""
        
        # Generate reorder message if needed
        reorder_message = None
        if decision['action'] == 'intelligent_reorder':
            reorder_message = {
                'timestamp': datetime.now().isoformat(),
                'action': 'REORDER',
                'item': 'Electronics_DEMO_ITEM',
                'quantity': decision['order_quantity'],
                'urgency': decision['urgency_level'],
                'reason': decision['reason'],
                'supplier': 'SUPPLIER_001',
                'estimated_cost': f"${decision['order_quantity'] * 30:,.2f}",
                'expected_delivery': (datetime.now() + timedelta(days=3)).isoformat()
            }
        
        # Calculate profit
        profit = self.performance_metrics['total_revenue'] - self.performance_metrics['total_costs']
        
        return {
            'status': 'success',
            'day': self.current_day,
            'timestamp': datetime.now().isoformat(),
            'agent_decision': {
                'action': decision['action'],
                'urgency_level': decision['urgency_level'],
                'reason': decision['reason'],
                'current_stock': decision['current_stock_after'],
                'order_quantity': decision.get('order_quantity', 0),
                'reorder_point': decision.get('adaptive_reorder_point', 0)
            },
            'reorder_message': reorder_message,
            'performance_metrics': {
                'service_level': round(self.performance_metrics['service_level'], 2),
                'total_revenue': round(self.performance_metrics['total_revenue'], 2),
                'total_costs': round(self.performance_metrics['total_costs'], 2),
                'profit': round(profit, 2),
                'orders_placed': self.performance_metrics['orders_placed'],
                'stockouts': self.performance_metrics['stockouts']
            },
            'system_info': {
                'uptime_seconds': (datetime.now() - self.service_start_time).total_seconds(),
                'total_decisions': self.total_decisions,
                'system_status': self.system_status
            }
        }
    
    def get_current_state(self):
        """Get current system state for monitoring"""
        
        recent_decisions = self.decision_log[-10:] if len(self.decision_log) >= 10 else self.decision_log
        
        return {
            'current_day': self.current_day,
            'current_stock': self.agent.current_stock,
            'performance_metrics': self.performance_metrics,
            'recent_decisions': recent_decisions,
            'system_uptime': (datetime.now() - self.service_start_time).total_seconds(),
            'status': self.system_status
        }

# Initialize the production service
production_service = ProductionAgentService()

# API Endpoints
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Intelligent Inventory Agent',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': (datetime.now() - production_service.service_start_time).total_seconds()
    })

@app.route('/api/process-day', methods=['POST'])
def process_daily_data():
    """Main endpoint for processing daily data"""
    
    try:
        daily_data = request.get_json()
        
        if not daily_data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        # Process the data through the intelligent agent
        result = production_service.process_daily_data(daily_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/current-state', methods=['GET'])
def get_current_state():
    """Get current system state"""
    
    try:
        state = production_service.get_current_state()
        return jsonify(state)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/performance-summary', methods=['GET'])
def get_performance_summary():
    """Get comprehensive performance summary"""
    
    try:
        agent_metrics = production_service.agent.get_performance_metrics()
        
        return jsonify({
            'status': 'success',
            'days_processed': production_service.current_day,
            'service_metrics': production_service.performance_metrics,
            'agent_metrics': agent_metrics,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_system():
    """Reset the system for new simulation"""
    
    try:
        global production_service
        production_service = ProductionAgentService()
        
        return jsonify({
            'status': 'success',
            'message': 'System reset successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Production Agent Service...")
    print("📡 API Endpoints available:")
    print("   • POST /api/process-day - Process daily data")
    print("   • GET  /api/current-state - Get system state")
    print("   • GET  /api/health - Health check")
    print("   • GET  /api/performance-summary - Performance metrics")
    print("   • POST /api/reset - Reset system")
    print("\n🎯 Service running on http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=True)