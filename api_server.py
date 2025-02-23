from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import time
import asyncio
from functools import partial

from brave_search.brave_search_function import web_search, parse_web_search_result
from web_page_parse.parse_web_function import parse_multiple_pages
from similiarity_search.chunck_split import chunk_split
from similiarity_search.ss_aml import embed_texts, embed_text
from similiarity_search.ss_faiss import faiss_search
from query_expand.qe_openai import expand_query

# Create FastAPI application
app = FastAPI(
    title="Web Search API",
    description="API for web search, text processing and similarity search",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class SearchResult(BaseModel):
    """Search result model"""
    text: str = Field(..., description="Content of the search result")
    url: str = Field(..., description="Source URL of the content")
    length: Optional[int] = Field(None, description="Length of the text content")

class SearchResponse(BaseModel):
    """Search response model"""
    results: List[SearchResult] = Field(..., description="List of search results")
    total_results: int = Field(..., description="Total number of results")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint for API status check"""
    return {"status": "running", "message": "Search API is running"}

async def async_search_pipeline(
    query: str,
    top_k: int = 5,
    chunk_size: int = 256,
    chunk_overlap: int = 50,
    verbose: bool = False
):
    """Asynchronous search pipeline implementation"""
    try:
        # 1. Query expansion
        expanded_query = expand_query(query)
        
        # 2. Web search
        search_result = await web_search(expanded_query)
        web_results, news_results = parse_web_search_result(search_result)
        
        if verbose:
            print(f"Found {len(web_results)} web results and {len(news_results)} news results")
        
        # 3. Collect URLs
        urls = [i['url'] for i in web_results + news_results]
        if verbose:
            print(f"Processing {len(urls)} URLs...")
        
        # 4. Parse pages
        results = await parse_multiple_pages(urls)
        
        # 5. Process results
        web_text_dict = {}
        for url, text, _ in results:
            if not text.strip():
                continue
            
            # Split text into chunks
            text_chunks = chunk_split(text, chunk_size=chunk_size, overlap=chunk_overlap)
            for chunk in text_chunks:
                if chunk.strip():
                    web_text_dict[chunk] = url
        
        # 6. Vectorize and search
        text_list = list(web_text_dict.keys())
        if not text_list:
            return [], {}
            
        vectors = embed_texts(text_list)
        query_vector = embed_text(query)
        similar_indices = faiss_search(query_vector, vectors, k=min(top_k, len(text_list)))
        
        # 7. Prepare results
        final_results = []
        for idx in similar_indices:
            text = text_list[idx]
            url = web_text_dict[text]
            final_results.append({
                'text': text,
                'url': url
            })
        
        return final_results, {}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search", response_model=SearchResponse)
async def search(
    query: str = Query(..., description="Search query text", min_length=1),
    top_k: int = Query(5, description="Number of results to return", ge=1, le=20),
    chunk_size: int = Query(256, description="Size of text chunks", ge=50, le=1000),
    chunk_overlap: int = Query(50, description="Overlap size between chunks", ge=0, le=200),
    verbose: bool = Query(False, description="Enable detailed logging")
) -> SearchResponse:
    """
    Execute search query and return results
    
    Parameters:
    - query: Search query text
    - top_k: Number of similar results to return (1-20)
    - chunk_size: Size of text chunks (50-1000)
    - chunk_overlap: Overlap size between chunks (0-200)
    - verbose: Enable detailed logging
    
    Returns:
    - SearchResponse: Response containing search results
    """
    try:
        # Call async search pipeline
        results, _ = await async_search_pipeline(
            query=query,
            top_k=top_k,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            verbose=verbose
        )
        
        # Process results
        search_results = []
        for result in results:
            search_results.append(
                SearchResult(
                    text=result["text"],
                    url=result["url"],
                    length=len(result["text"])
                )
            )
        
        # Build response
        response = SearchResponse(
            results=search_results,
            total_results=len(results)
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during search: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    # Start server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable hot reload in development
    )

"""
Sample curl commands for testing:

1. Basic search:
curl "http://localhost:8000/search?query=china+australia+relations"

2. Advanced search with all parameters:
curl "http://localhost:8000/search?query=china+australia+relations&top_k=10&chunk_size=300&chunk_overlap=50&verbose=true"

3. Health check:
curl "http://localhost:8000/health"

4. API status:
curl "http://localhost:8000/"

Note: For Windows PowerShell, replace single quotes with double quotes and escape inner quotes:
curl "http://localhost:8000/search?query=china+australia+relations"
""" 