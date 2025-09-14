# visualization_dashboard.py
# Comprehensive visualization and analytics dashboard

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime

class VisualizationDashboard:
    """Create comprehensive visualizations for inventory management system"""
    
    def __init__(self):
        # Set style for professional plots
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_comprehensive_dashboard(self, demo_data, simulation_results, orders_placed, save_path=None):
        """Create the main comprehensive dashboard"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 15))
        
        # Plot 1: Demand vs Inventory Management
        self._plot_inventory_management(ax1, demo_data, simulation_results, orders_placed)
        
        # Plot 2: Scenario Analysis
        self._plot_scenario_analysis(ax2, demo_data)
        
        # Plot 3: Agent Decision Intelligence
        self._plot_decision_intelligence(ax3, simulation_results)
        
        # Plot 4: Inventory Efficiency
        self._plot_inventory_efficiency(ax4, simulation_results)
        
        plt.suptitle('Intelligent Inventory Management System - Complete Analysis', 
                     fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Dashboard saved to {save_path}")
        
        plt.show()
        
    def _plot_inventory_management(self, ax, demo_data, simulation_results, orders_placed):
        """Plot inventory levels vs demand with intelligent decisions"""
        
        sim_df = pd.DataFrame(simulation_results)
        
        # Plot demand and inventory
        ax.plot(demo_data['Date'], demo_data['Sales'], label='Actual Demand', 
                color='blue', alpha=0.7, linewidth=1.5)
        ax.plot(sim_df['date'], sim_df['current_stock_after'], label='Inventory Level', 
                color='green', linewidth=2.5)
        ax.plot(sim_df['date'], sim_df['adaptive_reorder_point'], 
                label='Dynamic Reorder Point', color='red', linestyle='--', alpha=0.8)
        
        # Highlight intelligent orders
        if orders_placed:
            order_dates = [order['date'] for order in orders_placed]
            order_stocks = []
            for date in order_dates:
                matching_sim = sim_df[sim_df['date'] == date]
                if not matching_sim.empty:
                    order_stocks.append(matching_sim.iloc[0]['current_stock_after'])
                else:
                    order_stocks.append(1000)  # Default value
            
            ax.scatter(order_dates, order_stocks, color='red', s=120, marker='^', 
                      label='Intelligent Orders', zorder=5, edgecolors='darkred', linewidth=1)
        
        ax.set_title('Intelligent Inventory Management with Adaptive Thresholds', 
                     fontsize=14, fontweight='bold')
        ax.set_ylabel('Units', fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Add annotations for key events
        if len(demo_data) > 0:
            self._add_event_annotations(ax, demo_data, sim_df)
    
    def _plot_scenario_analysis(self, ax, demo_data):
        """Plot scenario events and their impact"""
        
        scenario_colors = {
            'Normal_Operations': '#E8F4F8',
            'Viral_Social_Media_Boost': '#FF6B6B',
            'Celebrity_Endorsement_Spike': '#FF8E53',
            'Black_Friday_Mega_Event': '#8B5CF6',
            'Supply_Chain_Disruption': '#8B4513',
            'Economic_Downturn_Effect': '#6B7280',
            'Competitor_Stockout_Benefit': '#10B981',
            'Post_Holiday_Clearance': '#F59E0B'
        }
        
        for scenario, color in scenario_colors.items():
            scenario_data = demo_data[demo_data['Scenario_Name'] == scenario]
            if not scenario_data.empty:
                ax.scatter(scenario_data['Date'], scenario_data['Sales'], 
                          color=color, label=scenario.replace('_', ' '), 
                          alpha=0.7, s=40, edgecolors='white', linewidth=0.5)
        
        ax.set_title('Demo Scenarios and Market Impact', fontsize=14, fontweight='bold')
        ax.set_ylabel('Daily Sales', fontsize=12)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
    def _plot_decision_intelligence(self, ax, simulation_results):
        """Plot agent decision intelligence distribution"""
        
        sim_df = pd.DataFrame(simulation_results)
        urgency_counts = sim_df['urgency_level'].value_counts()
        
        # Create a more sophisticated pie chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(urgency_counts)))
        wedges, texts, autotexts = ax.pie(urgency_counts.values, labels=urgency_counts.index, 
                                         autopct='%1.1f%%', startangle=90, colors=colors,
                                         explode=[0.05 if 'Critical' in label else 0 for label in urgency_counts.index])
        
        # Enhance text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        
        ax.set_title('Agent Decision Intelligence Distribution', 
                     fontsize=14, fontweight='bold')
        
    def _plot_inventory_efficiency(self, ax, simulation_results):
        """Plot inventory efficiency over time"""
        
        sim_df = pd.DataFrame(simulation_results)
        
        # Plot inventory level with fill
        ax.plot(sim_df['date'], sim_df['current_stock_after'], 
                label='Inventory Level', color='green', linewidth=2)
        ax.fill_between(sim_df['date'], 0, sim_df['current_stock_after'], 
                       alpha=0.3, color='green')
        
        # Add average reorder point
        avg_reorder = sim_df['adaptive_reorder_point'].mean()
        ax.axhline(y=avg_reorder, color='red', linestyle='--', linewidth=2,
                  label=f'Avg Reorder Point ({avg_reorder:.0f})')
        
        # Add efficiency zones
        max_stock = sim_df['current_stock_after'].max()
        ax.axhspan(0, avg_reorder * 0.5, alpha=0.1, color='red', label='Critical Zone')
        ax.axhspan(avg_reorder * 0.5, avg_reorder, alpha=0.1, color='yellow', label='Caution Zone')
        ax.axhspan(avg_reorder, max_stock, alpha=0.1, color='green', label='Safe Zone')
        
        ax.set_title('Inventory Efficiency Over Time', fontsize=14, fontweight='bold')
        ax.set_ylabel('Stock Units', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
    def _add_event_annotations(self, ax, demo_data, sim_df):
        """Add annotations for key events"""
        
        # Find major spikes
        demand_threshold = demo_data['Sales'].quantile(0.95)
        major_events = demo_data[demo_data['Sales'] > demand_threshold]
        
        for _, event in major_events.head(3).iterrows():  # Annotate top 3 events
            if event['Scenario_Name'] != 'Normal_Operations':
                ax.annotate(f"{event['Scenario_Name'].replace('_', ' ')}\n{event['Sales']:.0f} units",
                           xy=(event['Date'], event['Sales']),
                           xytext=(10, 20), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                           fontsize=9, fontweight='bold')
    
    def create_performance_timeline(self, simulation_results, save_path=None):
        """Create a detailed performance timeline"""
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12))
        
        sim_df = pd.DataFrame(simulation_results)
        
        # Timeline 1: Stock levels and actions
        self._plot_stock_timeline(ax1, sim_df)
        
        # Timeline 2: Demand prediction vs actual
        self._plot_demand_accuracy(ax2, sim_df)
        
        # Timeline 3: Scenario adaptation
        self._plot_scenario_timeline(ax3, sim_df)
        
        plt.suptitle('Agent Performance Timeline Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Performance timeline saved to {save_path}")
        
        plt.show()
        
    def _plot_stock_timeline(self, ax, sim_df):
        """Plot detailed stock level timeline"""
        
        ax.plot(sim_df['date'], sim_df['current_stock_after'], 
                label='Stock Level', color='green', linewidth=2)
        
        # Highlight reorder events
        reorders = sim_df[sim_df['action'] == 'intelligent_reorder']
        if not reorders.empty:
            ax.scatter(reorders['date'], reorders['current_stock_after'], 
                      color='red', s=100, marker='^', label='Reorders', zorder=5)
        
        # Highlight stockouts
        stockouts = sim_df[sim_df['action'] == 'stockout']
        if not stockouts.empty:
            ax.scatter(stockouts['date'], stockouts['current_stock_after'], 
                      color='darkred', s=100, marker='x', label='Stockouts', zorder=5)
        
        ax.set_title('Stock Level Timeline with Agent Actions')
        ax.set_ylabel('Units')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def _plot_demand_accuracy(self, ax, sim_df):
        """Plot demand prediction accuracy"""
        
        if 'actual_demand' in sim_df.columns:
            ax.plot(sim_df['date'], sim_df['predicted_demand'], 
                   label='Predicted Demand', color='blue', alpha=0.7)
            ax.plot(sim_df['date'], sim_df['actual_demand'], 
                   label='Actual Demand', color='orange', alpha=0.7)
            
            # Calculate and show accuracy
            accuracy = 100 - np.mean(np.abs(sim_df['predicted_demand'] - sim_df['actual_demand']) / 
                                   sim_df['actual_demand'] * 100)
            ax.text(0.02, 0.98, f'Prediction Accuracy: {accuracy:.1f}%', 
                   transform=ax.transAxes, fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        else:
            ax.plot(sim_df['date'], sim_df['predicted_demand'], 
                   label='Predicted Demand', color='blue')
        
        ax.set_title('Demand Forecasting Accuracy')
        ax.set_ylabel('Units')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def _plot_scenario_timeline(self, ax, sim_df):
        """Plot scenario adaptation timeline"""
        
        # Create color map for urgency levels
        urgency_colors = {
            'Normal': '#E8F4F8',
            'Conservative - Economic Risk': '#6B7280',
            'Caution - Supply Issues': '#F59E0B',
            'Opportunity - Market Capture': '#10B981',
            'Critical - Viral Event': '#FF6B6B',
            'Critical - Black Friday': '#8B5CF6',
            'Clearance Mode': '#F59E0B'
        }
        
        # Plot urgency levels as colored background
        for i, row in sim_df.iterrows():
            urgency = row['urgency_level']
            color = urgency_colors.get(urgency, '#E8F4F8')
            ax.axvspan(row['date'], row['date'] + pd.Timedelta(days=1), 
                      color=color, alpha=0.6)
        
        # Add reorder point line
        ax.plot(sim_df['date'], sim_df['adaptive_reorder_point'], 
               label='Adaptive Reorder Point', color='red', linewidth=2)
        
        ax.set_title('Scenario Adaptation Timeline')
        ax.set_ylabel('Reorder Threshold')
        ax.set_xlabel('Date')
        ax.grid(True, alpha=0.3)
        
        # Create custom legend for urgency levels
        handles = [plt.Rectangle((0,0),1,1, color=color, alpha=0.6) 
                  for color in urgency_colors.values()]
        labels = list(urgency_colors.keys())
        ax.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    def create_scenario_comparison(self, scenario_performance, save_path=None):
        """Create scenario comparison charts"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        scenarios = list(scenario_performance.keys())
        
        # Chart 1: Fulfillment rates by scenario
        fulfillment_rates = [scenario_performance[s]['fulfillment_rate'] for s in scenarios]
        ax1.bar(scenarios, fulfillment_rates, color='skyblue', edgecolor='navy')
        ax1.set_title('Fulfillment Rate by Scenario')
        ax1.set_ylabel('Fulfillment Rate (%)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Chart 2: Average demand by scenario
        avg_demands = [scenario_performance[s]['avg_demand'] for s in scenarios]
        ax2.bar(scenarios, avg_demands, color='lightcoral', edgecolor='darkred')
        ax2.set_title('Average Demand by Scenario')
        ax2.set_ylabel('Average Daily Demand')
        ax2.tick_params(axis='x', rotation=45)
        
        # Chart 3: Orders placed by scenario
        orders_placed = [scenario_performance[s]['orders_placed'] for s in scenarios]
        ax3.bar(scenarios, orders_placed, color='lightgreen', edgecolor='darkgreen')
        ax3.set_title('Orders Placed by Scenario')
        ax3.set_ylabel('Number of Orders')
        ax3.tick_params(axis='x', rotation=45)
        
        # Chart 4: Stockout rates by scenario
        stockout_rates = [scenario_performance[s]['stockout_rate'] for s in scenarios]
        ax4.bar(scenarios, stockout_rates, color='orange', edgecolor='darkorange')
        ax4.set_title('Stockout Rate by Scenario')
        ax4.set_ylabel('Stockout Rate (%)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.suptitle('Scenario Performance Comparison', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Scenario comparison saved to {save_path}")
        
        plt.show()