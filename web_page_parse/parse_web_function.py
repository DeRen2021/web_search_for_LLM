import trafilatura
import asyncio
import aiohttp
import requests
from typing import List, Tuple, Optional
import time

# Timeout settings
HTTP_TIMEOUT = 3  # HTTP request timeout in seconds
PARSE_TIMEOUT = 3  # Total parsing timeout in seconds

async def async_fetch_url(url: str, session: aiohttp.ClientSession) -> Optional[str]:
    """
    Asynchronously fetch URL content with timeout
    """
    try:
        timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT)
        async with session.get(url, timeout=timeout) as response:
            if response.status == 200:
                return await response.text()
    except asyncio.TimeoutError:
        print(f"Request timeout {url}: exceeded {HTTP_TIMEOUT} seconds")
    except Exception as e:
        print(f"Error fetching URL {url}: {str(e)}")
    return None

async def async_parse_web_page(url: str, session: aiohttp.ClientSession) -> Tuple[str, str, float]:
    """
    Asynchronously parse webpage with timeout
    """
    start_time = time.time()
    
    try:
        # Use asyncio.wait_for to add overall timeout
        downloaded = await asyncio.wait_for(
            async_fetch_url(url, session),
            timeout=PARSE_TIMEOUT
        )
        
        if not downloaded:
            return url, "", time.time() - start_time
        
        # Extract text (synchronous operation, but included in total timeout)
        extracted_text = trafilatura.extract(
            downloaded,
            favor_precision=True,
            include_comments=False,
            include_tables=False,
            output_format="txt"
        )
        
        parse_time = time.time() - start_time
        return url, extracted_text or "", parse_time
        
    except asyncio.TimeoutError:
        print(f"Parsing timeout {url}: exceeded {PARSE_TIMEOUT} seconds")
        return url, "", time.time() - start_time
    except Exception as e:
        print(f"Error parsing {url}: {str(e)}")
        return url, "", time.time() - start_time

async def parse_web_pages_parallel(urls: List[str]) -> List[Tuple[str, str, float]]:
    """
    Parse multiple webpages in parallel
    
    Args:
        urls: List of URLs to parse
    
    Returns:
        List[Tuple[str, str, float]]: List of (url, extracted_text, parse_time)
    """
    try:
        # Set client session default timeout
        timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [async_parse_web_page(url, session) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle any exceptions in results
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Error processing {urls[i]}: {str(result)}")
                    processed_results.append((urls[i], "", 0.0))
                else:
                    processed_results.append(result)
            
            return processed_results
            
    except Exception as e:
        print(f"Parallel processing error: {str(e)}")
        return [(url, "", 0.0) for url in urls]

def parse_web_page(url: str) -> str:
    """
    Synchronous function for parsing a single URL (for backward compatibility)
    """
    try:
        # Use requests for synchronous request with timeout
        response = requests.get(url, timeout=HTTP_TIMEOUT)
        if response.status_code != 200:
            return ""
            
        # Parse content with trafilatura
        extracted_text = trafilatura.extract(
            response.text,
            favor_precision=True,
            include_comments=False,
            include_tables=False,
            output_format="txt"
        )
        return extracted_text or ""
    except requests.Timeout:
        print(f"Request timeout {url}: exceeded {HTTP_TIMEOUT} seconds")
        return ""
    except Exception as e:
        print(f"Error parsing {url}: {str(e)}")
        return ""

async def parse_multiple_pages(urls: List[str]) -> List[Tuple[str, str, float]]:
    """
    Asynchronous wrapper for parallel page parsing
    
    Args:
        urls: List of URLs to parse
    
    Returns:
        List[Tuple[str, str, float]]: List of (url, extracted_text, parse_time)
    """
    return await parse_web_pages_parallel(urls)