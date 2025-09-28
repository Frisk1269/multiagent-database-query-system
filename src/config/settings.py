from smolagents import InferenceClientModel
from sqlalchemy import create_engine
from tools.tools import make_sql_engine, make_sql_to_dataframe

def create_model_config(engine):
    model_config = {
        "orchestrator": {
            "name": "orchestrator_agent",
            "model": InferenceClientModel(),
            "description": (
                "Orchestrator that manages the BI and Analysis agents. "
                "Routes business questions through the proper workflow: "
                "Business question -> SQL generation -> Data analysis -> Insights & recommendations"
            ),
            "tools": [
                make_sql_engine(engine),
                make_sql_to_dataframe(engine)
            ],
            "authorized_imports": ["json", "time"],
        },
        "analyst": {
            "name": "data_analysis_agent",
            "model": InferenceClientModel(),
            "description": (
                    "Data Analysis Agent that processes SQL results, creates DataFrames, "
                    "performs analysis, and generates visualizations and insights."
                ),
            "tools": [make_sql_to_dataframe(engine)],
            "authorized_imports": [
                    "pandas", "pandas.*", "numpy", "numpy.*", "json", "plotly",
                    "plotly.express", "plotly.graph_objects", "datetime", "statistics"
            ],
        },
        "business_intelligence": {
            "name": "business_intelligence_agent",
            "model": InferenceClientModel(),
            "description": (
                    "Business Intelligence Agent that translates business questions into SQL queries. "
                    "This agent understands business terminology, maps it to database schema, "
                    "and generates appropriate SQL queries with business context."
                ),
            "tools": [make_sql_engine(engine)],
            "authorized_imports": ["datetime", "json", "sqlalchemy"]
        }
    }
    return model_config