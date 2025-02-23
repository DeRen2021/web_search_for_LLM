import aisuite as ai
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.setting import OPENAI_API_KEY

client = ai.Client()

model = "openai:gpt-4o"

sys_prompt = """
You are a assistant. Give a user query, you job is to generate a query for web search. 
The query then will be used to search the web
to find relevant results, which will then be use as context to helpanswer user query.
Please onlt return the query, no other text.
"""

def expand_query(query: str, models: str = model) -> str:
    """
    Expand a user query using OpenAI's GPT model.
    
    Args:
        query (str): The original user query
        models (str, optional): The model to use. Defaults to model.
        
    Returns:
        str: The expanded query
    """
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": query}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.75
    )
    return response.choices[0].message.content

# For testing purposes
if __name__ == "__main__":
    test_query = "What is the capital of France?"
    print(expand_query(test_query))


