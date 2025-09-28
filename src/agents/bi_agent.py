
# Business Intelligence Agent (replaces planning agent with better focus)

class BusinessIntelligenceAgent:
    def __init__(self, db_manager: DbManager)
bi_agent = CodeAgent(
    name="business_intelligence_agent",
    model=InferenceClientModel(),
    description=(
        "Business Intelligence Agent that translates business questions into SQL queries. "
        "This agent understands business terminology, maps it to database schema, "
        "and generates appropriate SQL queries with business context."
    ),
    tools=[sql_engine],
    additional_authorized_imports=["datetime", "json", "sqlalchemy"],
)
bi_prompt = """
You are a Business Intelligence SQL Agent. Your role is to convert natural language business questions into accurate, efficient SQL using only the provided schema.

Explicit rules you must follow:

Use only given tables/columns.
Return SQL in a Python code block with triple quotes.
Keep queries clean, well-aliased, and optimized.
If impossible with schema, reply: "Cannot generate query: [reason]."
No explanations unless asked.

Example:

Schema:
orders(order_id, customer_id, order_date, total_amount)
customers(customer_id, name, region)

Q: "Which region had the highest sales last quarter?"

A:
query = '''
SELECT c.region, SUM(o.total_amount) AS total_sales
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date BETWEEN DATE '2024-04-01' AND DATE '2024-06-30'
GROUP BY c.region
ORDER BY total_sales DESC
LIMIT 1;
'''

"""

bi_agent.prompt_templates['system_prompt'] += bi_prompt