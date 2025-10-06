
from smolagents import CodeAgent

# Business Intelligence Agent (replaces planning agent with better focus)
class BusinessIntelligenceAgent:
    def __init__(self, model_config: dict, table_schemas):
        self.agent = CodeAgent(
            name=model_config['name'],
            model=model_config['model'],
            description=model_config["description"],
            tools=(model_config["tools"] if model_config and "tools" in model_config else []),
            additional_authorized_imports=(model_config["authorized_imports"] if model_config and "authorized_imports" in model_config else []),
        )
        self.bi_prompt = f"""
        You are a Business Intelligence SQL Agent. Your role is to convert natural language business questions into accurate, efficient SQL using only the provided schema.

        Explicit rules you must follow:

        Use only given tables/columns.
        Return SQL in a Python code block with triple quotes.
        Keep queries clean, well-aliased, and optimized.
        If impossible with schema, reply: "Cannot generate query: [reason]."
        No explanations unless asked.
        """

        self.agent.prompt_templates['system_prompt'] += self.bi_prompt
        
    def execute(self, query: str):
        return self.agent.run(query)