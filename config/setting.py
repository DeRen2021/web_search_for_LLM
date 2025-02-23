from dotenv import load_dotenv
import os

load_dotenv()

BRAVE_AI_API_KEY = os.getenv("BRAVE_AI_API_KEY")
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")