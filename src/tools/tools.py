from smolagents import tool
from sqlalchemy import text
# Improved SQL Engine Tool with validation
def make_sql_engine(engine, table_schemas):
  @tool
  def sql_engine(query: str) -> str:
      f"""
      Executes SQL queries on the database with schema validation.
      Returns a string representation of the result.

      Here are the tables' descriptions:

      {table_schemas}

      IMPORTANT:
      - Use only tables given to do the task
      - Use only columns available in the each table
      - You can derive new columns from available columns

      Args:
          query: The query to perform. This should be correct SQL.
      
      """

      try:
          with engine.connect() as conn:
              result = conn.execute(text(query))
              rows = result.fetchall()

              if not rows:
                  return "✅ Query executed successfully but returned no results."

              columns = result.keys()
              output = "✅ Query executed successfully!\n\nResults:\n"
              output += " | ".join(str(col) for col in columns) + "\n"
              output += "-" * (len(" | ".join(str(col) for col in columns))) + "\n"

              for row in rows:
                  output += " | ".join(str(val) for val in row) + "\n"

              return output

      except Exception as e:
          return f"❌ SQL EXECUTION ERROR: {str(e)}\n\nCheck your SQL syntax and ensure you're using the correct table/column names from the schema."

  return sql_engine

def make_sql_to_dataframe(engine):
  @tool
  def sql_to_dataframe(query: str) -> str:
    """
    Executes SQL query and converts results to pandas DataFrame for analysis.
    Returns JSON string containing DataFrame info and sample data.

    Args:
        query: The query to perform. This should be correct SQL.

    """
    try:
        import pandas as pd
        import json

        # Execute query and get DataFrame
        df = pd.read_sql_query(query, engine)

        if df.empty:
            return json.dumps({
                "status": "empty",
                "message": "Query returned no results",
                "columns": [],
                "sample_data": []
            })

        # Return structured info about the DataFrame
        result = {
            "status": "success",
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "sample_data": df.head(10).to_dict('records'),
            "summary_stats": df.describe().to_dict() if df.select_dtypes(include=['number']).shape[1] > 0 else {}
        }

        return json.dumps(result, default=str, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e)
        })
  return sql_to_dataframe