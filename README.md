# Intelligent Inventory Management System

An autonomous AI-driven inventory management system that combines machine learning forecasting with intelligent business rule engines to optimize inventory decisions in real-time.

## Overview

This project demonstrates the evolution from research prototype to production-ready system, showcasing two distinct implementations:

- **Version 1**: Modular research system for comprehensive analysis and validation
- **Version 2**: Production streaming architecture with microservices and real-time visualization

## System Architecture

### Core Components

The system uses a hybrid approach combining:
- **Prophet ML Model**: Bayesian time series forecasting for demand prediction
- **Intelligent Agent**: Rule-based decision engine with scenario adaptation
- **Scenario Engine**: Market event simulation (viral events, supply disruptions, competitor dynamics)
- **Performance Analytics**: Comprehensive metrics tracking and visualization

### Key Features

- **Autonomous Decision Making**: Agent makes inventory decisions without human intervention
- **Scenario Intelligence**: Adapts strategies based on market conditions (viral events, supply chain issues)
- **Real-time Processing**: Streaming data architecture with live dashboard updates
- **Measurable Outcomes**: Tracks service levels, profit optimization, and operational efficiency
- **Production Ready**: Microservices architecture with REST APIs and monitoring

## Quick Start

### Prerequisites

```bash
# Python 3.8+
# Virtual environment recommended
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Unix/Mac

# Install dependencies
pip install -r requirements.txt
```

### Version 1: Research System

```bash
cd core_modules
python main.py
```

Runs comprehensive 180-day simulation with detailed analytics and visualizations.

### Version 2: Production System

**Manual Microservices (Recommended for demonstrations):**

```bash
# Terminal 1 - Agent Service
cd streaming_production/services
python agent_service.py

# Terminal 2 - Dashboard
cd streaming_production/services
python dashboard_app.py

# Terminal 3 - Data Generator
cd streaming_production/services
python data_generator.py
```

**Automated Launch:**

```bash
cd streaming_production
python working_demo.py
```

Access live dashboard at http://localhost:5002

## Technical Implementation

### Forecasting Engine

Uses Facebook Prophet for demand forecasting:
- Learns seasonal patterns, trends, and volatility from historical data
- Bayesian inference with uncertainty quantification
- Handles multiple seasonality patterns (yearly, weekly, monthly)
- Automatic changepoint detection for trend shifts

### Decision Intelligence

Rule-based agent with scenario adaptation:
- Base reorder logic with dynamic threshold adjustment
- Scenario-specific strategies (2.5x inventory for viral events, conservative ordering during economic uncertainty)
- Multi-objective optimization (service level + cost + risk management)
- Performance tracking and continuous operation

### Production Architecture

Microservices design:
- **Agent Service** (Port 5001): REST API for inventory decisions
- **Dashboard Service** (Port 5002): Real-time monitoring and visualization
- **Data Generator**: Streaming market scenarios and business events
- **Event-driven communication** with JSON APIs

## Performance Results

The system demonstrates measurable business value:

- **100% Service Level**: Zero stockouts across 180-day simulation
- **$981,095 Profit**: Optimized inventory costs while maintaining availability
- **Scenario Adaptation**: Successfully handled viral events (4x demand spikes), supply disruptions, and competitive dynamics
- **Autonomous Operation**: 84.4% normal operations with intelligent escalation for critical events

## Use Cases

### Retail Inventory Optimization
- Seasonal demand planning
- Promotional event preparation
- Supply chain risk management

### Production Planning
- Multi-stage manufacturing
- Just-in-time inventory strategies
- Constraint identification and optimization

### Future Research Directions
- Integration with Theory of Constraints for multi-stage optimization
- Application to knowledge work and development team capacity planning
- Advanced constraint identification across complex systems

## File Structure

```
intelligent_inventory_system/
├── core_modules/                    # Version 1: Research system
│   ├── demand_forecaster.py        # Prophet-based forecasting
│   ├── inventory_agent.py          # Intelligent decision engine
│   ├── pattern_extractor.py        # Real pattern extraction
│   ├── synthetic_generator.py      # Scenario data generation
│   ├── visualization_dashboard.py  # Analytics and reporting
│   └── main.py                     # System integration
├── streaming_production/           # Version 2: Production system
│   ├── services/
│   │   ├── agent_service.py       # REST API microservice
│   │   ├── dashboard_app.py       # Live monitoring dashboard
│   │   └── data_generator.py      # Real-time data streaming
│   ├── templates/
│   │   └── dashboard.html         # Web interface
│   └── working_demo.py            # Automated system launcher
├── results/                       # Generated visualizations
└── requirements.txt              # Dependencies
```

## Technical Stack

- **Machine Learning**: Facebook Prophet (Bayesian time series)
- **Backend**: Python, Flask, REST APIs
- **Frontend**: HTML/CSS/JavaScript with real-time updates
- **Data Processing**: Pandas, NumPy, SciPy
- **Visualization**: Matplotlib, Plotly
- **Architecture**: Microservices, event-driven design

## Business Value

This system addresses real enterprise challenges:
- **Inventory optimization** is a multi-billion dollar problem in retail and manufacturing
- **Autonomous decision-making** reduces human error and operational costs
- **Real-time adaptation** enables rapid response to market changes
- **Measurable ROI** through service level maintenance and cost optimization

## Contributing

This project demonstrates progression from academic research to production deployment, showcasing:
- Modular software architecture
- Hybrid ML/rule-based systems
- Microservices design patterns
- Real-time data processing
- Enterprise deployment considerations

## License

Academic/Research Project - ELVTR AI Solution Architect Capstone

## Contact

Developed as part of ELVTR AI Solution Architect certification program.