from smolagents import tool
from sqlalchemy import text
# Improved SQL Engine Tool with validation
def make_sql_engine(engine):
  @tool
  def sql_engine(query: str) -> str:
      """
      Executes SQL queries on the database with schema validation.
      Returns a string representation of the result.

      Here are the tables' descriptions:

      transactions:
        - transaction_id (INTEGER)          -- unique transaction record
        - customer_id (INTEGER)             -- links to customers
        - employee_id (INTEGER)             -- links to employees (who sold it)
        - approver_id (INTEGER)             -- approving manager, if applicable
        - product_id (INTEGER)              -- links to products
        - transaction_type_id (INTEGER)     -- links to transaction_types
        - total_amount (FLOAT)              -- full value of the transaction
        - remaining_amount (FLOAT)          -- unpaid balance. If > 0, customer still owes money
        - created_at (DATETIME)             -- when transaction was created
        - due_at (DATETIME)                 -- payment due date

      customers:
        - customer_id (INTEGER)
        - customer_name (VARCHAR)
        - category_id (INTEGER)

      employees:
        - employee_id (INTEGER)
        - employee_name (VARCHAR)
        - job_desk_id (INTEGER)
        - department_id (INTEGER)

      transaction_types:
        - transaction_type_id (INTEGER)
        - transaction_type_name (VARCHAR)   -- fixed values: 'purchase', 'refund', 'credit', 'installments', 'service'

      products:
        - product_id (INTEGER)
        - product_name (VARCHAR)
        - price (FLOAT)
        - stock (INTEGER)

      departments:
        - department_id (INTEGER)
        - department_name (VARCHAR)
        - department_size (INTEGER)

      business_category:
        - category_id (INTEGER)
        - category_name (VARCHAR)

      job_desk:
        - job_desk_id (INTEGER)
        - job_desk_name (VARCHAR)

      DEFINITIONS / BUSINESS LOGIC:
      - **Overdue payment**: A transaction is overdue if:
        1. `remaining_amount > 0` (customer still owes money)
        2. `due_at < CURRENT_DATE` (the due date has already passed)
      - **Relevant transaction types**: Only `credit` and `installments` transactions can become overdue.
        Purchases are usually fully paid, refunds reduce balances, and services may not have installments.
      - **Amount still owed**: Taken from `transactions.remaining_amount`.
      - **Who sold it**: The `employee_id` in `transactions` joins to `employees.employee_name`.
      - **Days overdue**: Use `julianday('now') - julianday(transactions.due_at)` in SQLite.

      IMPORTANT:
      - There are NO tables named 'payments', 'installments', 'credit_transactions', or 'salesreps'.
      - Use `customers.customer_name`, not `CustomerName`.
      - Use `employees.employee_name`, not `SalesRepName`.
      - Use SQLite date functions (`julianday`, `datetime`, etc.).

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