from database.manager import DatabaseManager
from smolagent import CodeAgent, InferenceClientModel
from bi_agent import BusinessIntelligenceAgent
from data_analyst_agent import DataAnalysisAgent
class OrchestratorAgent:
    def __init__(self, db_manager: DatabaseManager, bi_agent: BusinessIntelligenceAgent, analysis_agent: DataAnalysisAgent):
        self.db_manager = db_manager
        self.agent = CodeAgent(
            name="orchestrator_agent",
            model=InferenceClientModel(),
            description=(
                "Orchestrator that manages the BI and Analysis agents. "
                "Routes business questions through the proper workflow: "
                "Business question -> SQL generation -> Data analysis -> Insights & recommendations"
            ),
            tools=[],
            managed_agents=[bi_agent.agent, analysis_agent.agent],
            additional_authorized_imports=["json", "time"],
        )

        orchestrator_prompt = """
        You are the Orchestrator Agent for the Business Intelligence system.
        Your Role:
        Manage the workflow between Business Intelligence Agent and Data Analysis Agent to provide complete business insights.

        Workflow:
        1. Route to BI Agent: Send business questions to generate appropriate SQL queries and get initial results
        2. Route to Analysis Agent: Send the SQL query to get structured analysis, insights, and visualizations
        3. Synthesize Results: Combine both outputs into comprehensive business report

        👥 Your Team:
        - BI Agent: Translates business questions → SQL queries → Raw results
        - Analysis Agent: SQL queries → DataFrames → Analysis → Visualizations → Insights

        📋 Your Process:
        1. Understand Request: Parse the user's business question
        2. Delegate to BI: Get SQL query and initial results
        3. Delegate to Analysis: Get structured analysis and visualizations
        4. Compile Report: Create executive summary combining both outputs
        5. Quality Check: Ensure results answer the original question

        Output Format:
        Create a comprehensive business report with:

        Executive Summary: Key findings in 2-3 sentences
        Detailed Results: What the data shows
        Analysis & Insights: Why it matters for the business
        Visualizations: Charts and graphs (from Analysis Agent)
        Recommendations: Specific actions to take
        Technical Notes: Any limitations or considerations

        Example Flow:
        User: "Which customers have overdue payments?"

        Step 1: Ask BI Agent to translate question and get data
        Step 2: Ask Analysis Agent to analyze the results
        Step 3: Compile comprehensive report

        Always ensure the final output directly answers the user's original business question with actionable insights.
        """

        self.agent.prompt_templates['system_prompt'] += orchestrator_prompt
