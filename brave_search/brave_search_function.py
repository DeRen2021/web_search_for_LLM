from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import json

BRAVE_SEARCH_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"

# load_dotenv()

# brave_ai_api_key = os.getenv("BRAVE_AI_API_KEY")
# brave_search_api_key = os.getenv("BRAVE_SEARCH_API_KEY")
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.setting import BRAVE_AI_API_KEY, BRAVE_SEARCH_API_KEY



        
async def web_search(query):
    async with aiohttp.ClientSession() as session:
        url = BRAVE_SEARCH_ENDPOINT
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": BRAVE_SEARCH_API_KEY
        }
        async with session.get(url, headers=headers, params={"q": query}) as response:
            search_result = await response.json()
            return search_result

def parse_web_search_result(result):
    search_result_type = {i['type'] for i in result['mixed']['main']}
    web_result = []
    news_result = []
    if 'web' in search_result_type:
        for i in result['web']['results']:
            web_result.append({
                'title': i['title'],
                'url': i['url'],
                'description': i['description']
            })
    if 'news' in search_result_type:
        for i in result['news']['results']:
            news_result.append({
                'title': i['title'],
                'url': i['url'],
                'description': i.get('description', ''),
                'age': i.get('age', '')
            })
    return web_result, news_result

# 同步包装函数
def search_and_parse(query):
    """
    同步调用搜索和解析函数的包装器
    """
    async def run_search():
        result = await web_search(query)
        return parse_web_search_result(result)
    
    return asyncio.run(run_search())