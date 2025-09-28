# NL2SQL Multi-Agent System
A production-ready system that converts natural language questions into SQL queries using a multi-agent architecture built with the smolagents framework.
![alt text](https://github.com/jonuts100/multi-database-query-system/blob/main/img1.png?raw=True)
![alt text](https://github.com/jonuts100/multi-database-query-system/blob/main/img2.png?raw=True)
![alt text](https://github.com/jonuts100/multi-database-query-system/blob/main/img3.png?raw=True)
![alt text](https://github.com/jonuts100/multi-database-query-system/blob/main/img4.png?raw=True)
## Overview
This system employs three specialized AI agents working together to understand natural language questions, generate optimized SQL queries, and provide comprehensive data analysis. Unlike traditional NL2SQL solutions, this multi-agent approach provides better query validation, optimization suggestions, and business intelligence insights.
Key Features

Multi-Agent Architecture: Specialized agents for query generation, validation, and analysis
Schema-Aware Generation: Validates queries against actual database schemas
Query Optimization: Suggests performance improvements and best practices
Multiple Database Support: Works with SQLite, PostgreSQL, MySQL, and more
Production Ready: Comprehensive error handling, logging, and monitoring
REST API: Easy integration with existing applications
Docker Support: Containerized deployment with docker-compose
Comprehensive Testing: Unit tests, integration tests, and performance benchmarks

## Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Orchestrator  │    │ Business Intel   │    │ Data Analysis   │
│     Agent       │◄──►│     Agent        │◄──►│     Agent       │
│                 │    │                  │    │                 │
│ Manages workflow│    │ Generates SQL    │    │ Analyzes results│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   SQL Engine    │
                    │   & Database    │
                    └─────────────────┘
```
## Quick Start
### Prerequisites

- Python 3.9+
- HuggingFace API key (for smolagents)

### Installation
```
# Clone the repository
git clone https://github.com/yourusername/nl2sql-multiagent-system.git
cd nl2sql-multiagent-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

#### Install dependencies
pip install -r requirements.txt

#### Set up environment variables
cp .env.example .env
#### Edit .env with your API keys
```
## Basic Usage
```
from src.agents.orchestrator import OrchestratorAgent
from src.database.manager import DatabaseManager
from src.config import AppConfig

# Initialize components
config = AppConfig()
db_manager = DatabaseManager(config.database.url)
orchestrator = OrchestratorAgent(db_manager, config)

# Ask a question
result = orchestrator.execute_query("What are the top 10 customers by revenue?")
print(result)
```
## REST API
```
# Start the API server
python -m src.api

# Query via HTTP
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me customers with overdue payments"}'
```
## Docker Deployment
```
# Build and run with docker-compose
docker-compose up -d

# Check status
docker-compose ps
```
## Example Queries
The system handles various types of business intelligence queries:
```
# Sales Analysis
"What were our top 5 products by revenue last quarter?"

# Customer Analytics  
"Which customers have the highest outstanding debt?"

# Operational Queries
"Show me all transactions that are overdue by more than 30 days"

# Trend Analysis
"How has our monthly revenue changed over the past year?"
```
