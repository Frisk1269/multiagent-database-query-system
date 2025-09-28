from agents.bi_agent import BusinessIntelligenceAgent
from agents.data_analyst_agent import DataAnalysisAgent
from agents.orchestrator_agent import OrchestratorAgent
from config.settings import create_model_config
from database.manager import DatabaseManager

def __init__():
    engine = DatabaseManager(connection_string="sqlite:///mydb.sqlite")
    model_config = create_model_config(engine)
    query = input("Enter a query: ")
    
    business_intelligent_agent = BusinessIntelligenceAgent(model_config=model_config['business_intelligence'])
    data_analyst_agent = DataAnalysisAgent(model_config=model_config['analyst'])
    orchestrator_agent = OrchestratorAgent(model_config=model_config['orchestrator'], bi_agent=business_intelligent_agent, analysis_agent=data_analyst_agent)
    
    res = orchestrator_agent.execute(query)
    print(res)