# inventory_agent.py
# Intelligent inventory management agent with scenario adaptation

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class IntelligentInventoryAgent:
    """Advanced inventory agent that adapts to market scenarios"""
    
    def __init__(self, initial_stock=2000, base_reorder_point=300, base_reorder_quantity=800):
        # Inventory state
        self.current_stock = initial_stock
        self.base_reorder_point = base_reorder_point
        self.base_reorder_quantity = base_reorder_quantity
        
        # Agent memory and learning
        self.orders_placed = []
        self.stockouts = 0
        self.decisions_log = []
        self.scenario_memory = {}
        
        # Performance tracking
        self.total_revenue = 0
        self.total_costs = 0
        self.customer_satisfaction_score = 100
        
        # Configuration
        self.safety_stock_multiplier = 1.2
        self.max_order_size = 5000
        self.lead_time_days = 3
        
    def analyze_scenario_and_adapt(self, scenario_name, predicted_demand, current_date):
        """Intelligent adaptation based on scenario type and context"""
        
        # Default values
        reorder_point = self.base_reorder_point
        reorder_quantity = self.base_reorder_quantity
        urgency_level = "Normal"
        strategy_notes = "Standard operations"
        
        # Scenario-specific intelligent adaptations
        if "Viral" in scenario_name or "Celebrity" in scenario_name:
            # Massive demand spike expected - be aggressive
            reorder_point = self.base_reorder_point * 2.5
            reorder_quantity = min(self.base_reorder_quantity * 3, self.max_order_size)
            urgency_level = "Critical - Viral Event"
            strategy_notes = "Preparing for viral demand spike - maximizing availability"
            
        elif "Black_Friday" in scenario_name:
            # Known mega event - prepare well in advance
            reorder_point = self.base_reorder_point * 3
            reorder_quantity = min(self.base_reorder_quantity * 4, self.max_order_size)
            urgency_level = "Critical - Black Friday"
            strategy_notes = "Black Friday preparation - ensuring maximum stock availability"
            
        elif "Supply_Chain_Disruption" in scenario_name:
            # Conservative approach during supply uncertainty
            reorder_point = self.base_reorder_point * 1.8
            reorder_quantity = self.base_reorder_quantity * 0.7  # Smaller, more frequent orders
            urgency_level = "Caution - Supply Issues"
            strategy_notes = "Supply chain disruption - smaller orders to reduce risk"
            
        elif "Economic_Downturn" in scenario_name:
            # Reduce inventory to minimize financial risk
            reorder_point = self.base_reorder_point * 0.7
            reorder_quantity = self.base_reorder_quantity * 0.6
            urgency_level = "Conservative - Economic Risk"
            strategy_notes = "Economic downturn - minimizing inventory investment"
            
        elif "Competitor_Stockout" in scenario_name:
            # Opportunity to capture extra market share
            reorder_point = self.base_reorder_point * 1.5
            reorder_quantity = min(self.base_reorder_quantity * 2, self.max_order_size)
            urgency_level = "Opportunity - Market Capture"
            strategy_notes = "Competitor stockout - capturing increased market share"
            
        elif "Post_Holiday" in scenario_name:
            # Clearance period - minimal restocking
            reorder_point = self.base_reorder_point * 0.5
            reorder_quantity = self.base_reorder_quantity * 0.4
            urgency_level = "Clearance Mode"
            strategy_notes = "Post-holiday clearance - minimal restocking"
            
        # Store scenario learning for future use
        self._update_scenario_memory(scenario_name, predicted_demand, urgency_level)
        
        return {
            'reorder_point': reorder_point,
            'reorder_quantity': reorder_quantity,
            'urgency_level': urgency_level,
            'strategy_notes': strategy_notes
        }
    
    def _update_scenario_memory(self, scenario_name, demand, urgency_level):
        """Update agent's memory of scenario patterns"""
        
        if scenario_name not in self.scenario_memory:
            self.scenario_memory[scenario_name] = {
                'encounters': 0,
                'avg_demand': 0,
                'max_demand': 0,
                'successful_strategies': []
            }
        
        memory = self.scenario_memory[scenario_name]
        memory['encounters'] += 1
        memory['avg_demand'] = ((memory['avg_demand'] * (memory['encounters'] - 1)) + demand) / memory['encounters']
        memory['max_demand'] = max(memory['max_demand'], demand)
        memory['successful_strategies'].append(urgency_level)
    
    def make_intelligent_decision(self, predicted_demand, current_date, scenario_name="Normal_Operations"):
        """Main agent decision-making logic with full intelligence"""
        
        # Ensure positive predicted demand
        predicted_demand = max(0, predicted_demand)
        
        # Get scenario-adapted parameters
        adaptation = self.analyze_scenario_and_adapt(scenario_name, predicted_demand, current_date)
        
        # Initialize decision record
        decision = {
            'date': current_date,
            'scenario': scenario_name,
            'predicted_demand': predicted_demand,
            'current_stock_before': self.current_stock,
            'urgency_level': adaptation['urgency_level'],
            'strategy_notes': adaptation['strategy_notes'],
            'adaptive_reorder_point': adaptation['reorder_point'],
            'adaptive_reorder_quantity': adaptation['reorder_quantity'],
            'action': 'no_action',
            'order_quantity': 0,
            'reason': '',
            'current_stock_after': self.current_stock
        }
        
        # Simulate actual demand with realistic variance
        demand_variance = np.random.normal(0, abs(predicted_demand) * 0.1)
        actual_demand = max(0, predicted_demand + demand_variance)
        
        # Process daily demand
        demand_fulfilled, stockout_amount = self._process_demand(actual_demand)
        
        if stockout_amount > 0:
            self.stockouts += 1
            self.customer_satisfaction_score = max(0, self.customer_satisfaction_score - 2)
            decision['action'] = 'stockout'
            decision['reason'] = f'Stockout: {stockout_amount:.0f} units unfulfilled'
        
        # Update decision with post-demand stock level
        decision['current_stock_after'] = self.current_stock
        decision['actual_demand'] = actual_demand
        decision['demand_fulfilled'] = demand_fulfilled
        
        # Intelligent reorder decision
        if self.current_stock <= adaptation['reorder_point']:
            order_quantity = self._calculate_smart_order_quantity(
                adaptation['reorder_quantity'], 
                predicted_demand, 
                scenario_name
            )
            
            # Place order
            self.current_stock += order_quantity
            self._record_order(current_date, order_quantity, scenario_name, adaptation['urgency_level'])
            
            decision['action'] = 'intelligent_reorder'
            decision['order_quantity'] = order_quantity
            decision['reason'] = f"Smart reorder: {adaptation['strategy_notes']}"
            decision['current_stock_after'] = self.current_stock
        
        # Log decision
        self.decisions_log.append(decision)
        
        return decision
    
    def _process_demand(self, actual_demand):
        """Process daily demand and handle stockouts"""
        
        if self.current_stock >= actual_demand:
            self.current_stock -= actual_demand
            self.total_revenue += actual_demand * 50  # Assume $50 per unit
            return actual_demand, 0
        else:
            # Partial fulfillment
            fulfilled = self.current_stock
            stockout = actual_demand - fulfilled
            self.current_stock = 0
            self.total_revenue += fulfilled * 50
            return fulfilled, stockout
    
    def _calculate_smart_order_quantity(self, base_quantity, predicted_demand, scenario_name):
        """Calculate intelligent order quantity based on multiple factors"""
        
        # Base calculation
        order_quantity = base_quantity
        
        # Adjust based on current stock turnover rate
        if len(self.decisions_log) > 7:  # If we have at least a week of data
            recent_demand = [d['actual_demand'] for d in self.decisions_log[-7:] if 'actual_demand' in d]
            avg_weekly_demand = np.mean(recent_demand) * 7 if recent_demand else predicted_demand * 7
            
            # Order enough for 2-3 weeks based on scenario
            if "Critical" in scenario_name:
                weeks_coverage = 4  # Extra coverage for critical scenarios
            elif "Conservative" in scenario_name:
                weeks_coverage = 1.5  # Less coverage for conservative scenarios
            else:
                weeks_coverage = 2.5  # Standard coverage
                
            demand_based_quantity = avg_weekly_demand * weeks_coverage
            order_quantity = max(order_quantity, demand_based_quantity)
        
        # Cap at maximum order size
        order_quantity = min(order_quantity, self.max_order_size)
        
        return int(order_quantity)
    
    def _record_order(self, date, quantity, scenario, urgency):
        """Record order details for tracking and analysis"""
        
        order = {
            'date': date,
            'quantity': quantity,
            'scenario': scenario,
            'urgency': urgency,
            'cost': quantity * 30,  # Assume $30 cost per unit
            'lead_time_expected': self.lead_time_days
        }
        
        self.orders_placed.append(order)
        self.total_costs += order['cost']
    
    def get_performance_metrics(self):
        """Calculate comprehensive performance metrics"""
        
        total_days = len(self.decisions_log)
        if total_days == 0:
            return {}
        
        # Basic metrics
        stockout_rate = (self.stockouts / total_days) * 100
        service_level = ((total_days - self.stockouts) / total_days) * 100
        
        # Financial metrics
        profit = self.total_revenue - self.total_costs
        profit_margin = (profit / self.total_revenue * 100) if self.total_revenue > 0 else 0
        
        # Inventory efficiency
        total_orders = len(self.orders_placed)
        avg_order_size = np.mean([order['quantity'] for order in self.orders_placed]) if self.orders_placed else 0
        total_ordered = sum([order['quantity'] for order in self.orders_placed])
        
        # Scenario adaptation metrics
        scenario_counts = {}
        for decision in self.decisions_log:
            scenario = decision['scenario']
            scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
        
        metrics = {
            'operational': {
                'total_days_simulated': total_days,
                'stockouts': self.stockouts,
                'stockout_rate_percent': round(stockout_rate, 2),
                'service_level_percent': round(service_level, 2),
                'customer_satisfaction': round(self.customer_satisfaction_score, 1)
            },
            'financial': {
                'total_revenue': round(self.total_revenue, 2),
                'total_costs': round(self.total_costs, 2),
                'profit': round(profit, 2),
                'profit_margin_percent': round(profit_margin, 2)
            },
            'inventory': {
                'current_stock': self.current_stock,
                'total_orders_placed': total_orders,
                'average_order_size': round(avg_order_size, 0),
                'total_units_ordered': total_ordered,
                'inventory_turnover_rate': round(total_ordered / max(1, self.current_stock), 2)
            },
            'intelligence': {
                'scenarios_encountered': len(scenario_counts),
                'scenario_breakdown': scenario_counts,
                'adaptive_decisions': len([d for d in self.decisions_log if d['urgency_level'] != 'Normal']),
                'learning_entries': len(self.scenario_memory)
            }
        }
        
        return metrics
    
    def get_scenario_performance(self):
        """Analyze performance by scenario type"""
        
        scenario_performance = {}
        
        for decision in self.decisions_log:
            scenario = decision['scenario']
            
            if scenario not in scenario_performance:
                scenario_performance[scenario] = {
                    'encounters': 0,
                    'stockouts': 0,
                    'orders_placed': 0,
                    'total_demand': 0,
                    'total_fulfilled': 0,
                    'urgency_levels': []
                }
            
            perf = scenario_performance[scenario]
            perf['encounters'] += 1
            perf['urgency_levels'].append(decision['urgency_level'])
            
            if 'actual_demand' in decision:
                perf['total_demand'] += decision['actual_demand']
            
            if 'demand_fulfilled' in decision:
                perf['total_fulfilled'] += decision['demand_fulfilled']
            
            if decision['action'] == 'stockout':
                perf['stockouts'] += 1
            elif decision['action'] == 'intelligent_reorder':
                perf['orders_placed'] += 1
        
        # Calculate derived metrics
        for scenario, perf in scenario_performance.items():
            if perf['encounters'] > 0:
                perf['stockout_rate'] = (perf['stockouts'] / perf['encounters']) * 100
                perf['avg_demand'] = perf['total_demand'] / perf['encounters']
                perf['fulfillment_rate'] = (perf['total_fulfilled'] / max(1, perf['total_demand'])) * 100
                perf['most_common_urgency'] = max(set(perf['urgency_levels']), key=perf['urgency_levels'].count)
        
        return scenario_performance
    
    def reset_simulation(self, initial_stock=None):
        """Reset agent state for new simulation"""
        
        if initial_stock:
            self.current_stock = initial_stock
        else:
            self.current_stock = 2000  # Default
            
        self.orders_placed = []
        self.stockouts = 0
        self.decisions_log = []
        self.total_revenue = 0
        self.total_costs = 0
        self.customer_satisfaction_score = 100
        
        print("🔄 Agent state reset for new simulation")
    
    def export_decisions_log(self, filepath):
        """Export decisions log to CSV for analysis"""
        
        if not self.decisions_log:
            print("❌ No decisions to export")
            return
            
        df = pd.DataFrame(self.decisions_log)
        df.to_csv(filepath, index=False)
        print(f"✅ Decisions log exported to {filepath}")
    
    def print_performance_summary(self):
        """Print a comprehensive performance summary"""
        
        metrics = self.get_performance_metrics()
        scenario_perf = self.get_scenario_performance()
        
        print("\n" + "="*60)
        print("🤖 INTELLIGENT INVENTORY AGENT PERFORMANCE SUMMARY")
        print("="*60)
        
        # Operational Performance
        print(f"\n📊 OPERATIONAL PERFORMANCE:")
        print(f"   • Days Simulated: {metrics['operational']['total_days_simulated']}")
        print(f"   • Service Level: {metrics['operational']['service_level_percent']}%")
        print(f"   • Stockout Rate: {metrics['operational']['stockout_rate_percent']}%")
        print(f"   • Customer Satisfaction: {metrics['operational']['customer_satisfaction']}/100")
        
        # Financial Performance
        print(f"\n💰 FINANCIAL PERFORMANCE:")
        print(f"   • Total Revenue: ${metrics['financial']['total_revenue']:,.2f}")
        print(f"   • Total Costs: ${metrics['financial']['total_costs']:,.2f}")
        print(f"   • Profit: ${metrics['financial']['profit']:,.2f}")
        print(f"   • Profit Margin: {metrics['financial']['profit_margin_percent']}%")
        
        # Inventory Management
        print(f"\n📦 INVENTORY MANAGEMENT:")
        print(f"   • Current Stock: {metrics['inventory']['current_stock']:,.0f} units")
        print(f"   • Orders Placed: {metrics['inventory']['total_orders_placed']}")
        print(f"   • Average Order Size: {metrics['inventory']['average_order_size']:,.0f} units")
        print(f"   • Inventory Turnover: {metrics['inventory']['inventory_turnover_rate']:.2f}")
        
        # Intelligence & Adaptation
        print(f"\n🧠 INTELLIGENCE & ADAPTATION:")
        print(f"   • Scenarios Encountered: {metrics['intelligence']['scenarios_encountered']}")
        print(f"   • Adaptive Decisions: {metrics['intelligence']['adaptive_decisions']}")
        print(f"   • Learning Entries: {metrics['intelligence']['learning_entries']}")
        
        # Scenario Breakdown
        print(f"\n🎯 SCENARIO PERFORMANCE:")
        for scenario, perf in scenario_perf.items():
            if perf['encounters'] > 0:
                print(f"   • {scenario}:")
                print(f"     - Encounters: {perf['encounters']}")
                print(f"     - Fulfillment Rate: {perf['fulfillment_rate']:.1f}%")
                print(f"     - Primary Strategy: {perf['most_common_urgency']}")
        
        print("="*60)