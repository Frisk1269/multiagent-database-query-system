from agents.bi_agent import BusinessIntelligenceAgent
from agents.data_analyst_agent import DataAnalysisAgent
from agents.orchestrator_agent import OrchestratorAgent
from config.settings import create_model_config
from database.manager import DatabaseManager
from database.connect import DatabaseConfig, SQLConnector
import os
from dotenv import load_dotenv
from huggingface_hub import login

load_dotenv()
hf_token = os.getenv("HUGGINGFACE_TOKEN")

def main():
    
    # Using sample data
    # engine = DatabaseManager(connection_string="sqlite:///mydb.sqlite")
    db_config = DatabaseConfig()
    
    engine = SQLConnector(db_config, auth_type='Windows')
    tables_summary = engine.db_schemas
    model_config = create_model_config(engine, table_schemas=tables_summary)

    query = input("Enter a query: ")

    #Initialize agents
    business_intelligence_agent = BusinessIntelligenceAgent(model_config=model_config['business_intelligence'])
    data_analyst_agent = DataAnalysisAgent(model_config=model_config['analyst'])
    orchestrator_agent = OrchestratorAgent(
        model_config=model_config['orchestrator'],
        bi_agent=business_intelligence_agent,
        analysis_agent=data_analyst_agent
    )

    # print(engine.display_table("transactions", 10))
    # print(model_config)
    res = orchestrator_agent.execute(query)
    print(res)

if __name__ == "__main__":
    main()