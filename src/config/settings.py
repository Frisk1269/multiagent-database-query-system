from smolagents import InferenceClientModel
from tools.tools import make_sql_engine, make_sql_to_dataframe
from database.connect import SQLConnector

MODEL = InferenceClientModel()
def create_model_config(engine, table_schemas):
    model_config = {
        "orchestrator": {
            "name": "orchestrator_agent",
            "model": MODEL,
            "description": (
                "Orchestrator that manages the BI and Analysis agents. "
                "Routes business questions through the proper workflow: "
                "Business question -> SQL generation -> Data analysis -> Insights & recommendations"
            ),
            "tools": [
                make_sql_engine(engine, table_schemas),
                make_sql_to_dataframe(engine)
            ],
            "authorized_imports": ["json", "time"],
        },
        "analyst": {
            "name": "data_analysis_agent",
            "model": MODEL,
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
            "model": MODEL,
            "description": (
                    "Business Intelligence Agent that translates business questions into SQL queries. "
                    "This agent understands business terminology, maps it to database schema, "
                    "and generates appropriate SQL queries with business context."
                ),
            "tools": [make_sql_engine(engine, table_schemas)],
            "authorized_imports": ["datetime", "json", "sqlalchemy"]
        }
    }
    return model_config

def create_db_config(engine: SQLConnector):
    
    table_info = engine.db_info # note: already a string
    table_schema_info = engine.get_table_schema()
    db_config = {
        "tables": table_info,
        "table_schemas": table_schema_info, 
    }
    return db_config
    
    
from database.connect import DatabaseConfig
if __name__ == '__main__':
    db_config = DatabaseConfig()
    engine = SQLConnector(db_config, auth_type='Windows')
    print(create_db_config())