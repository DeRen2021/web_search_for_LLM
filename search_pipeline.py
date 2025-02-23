from typing import List, Dict, Tuple
import time
from datetime import datetime

from brave_search.brave_search_function import search_and_parse
from web_page_parse.parse_web_function import parse_multiple_pages
from similiarity_search.chunck_split import chunk_split
from similiarity_search.ss_aml import embed_texts, embed_text
from similiarity_search.ss_faiss import faiss_search

from query_expand.qe_openai import expand_query

def search_pipeline(
    query: str,
    top_k: int = 5,
    verbose: bool = True
) -> Tuple[List[Dict], Dict[str, float]]:
    """
    完整的搜索管道，包括查询扩展、网页搜索、并行网页解析、向量化和相似度搜索
    
    Args:
        query: 原始查询文本
        top_k: 返回最相似的结果数量
        verbose: 是否打印详细信息
        
    Returns:
        Tuple[List[Dict], Dict[str, float]]: 
            - 包含相似文本和对应URL的结果列表
            - 包含各个阶段耗时的统计信息
    """
    stats = {}
    
    # 1. 查询扩展
    expanded_query = expand_query(query)

    
    # 2. 网页搜索
    start_time = time.time()
    web_results, news_results = search_and_parse(expanded_query)
    stats['web_search_time'] = time.time() - start_time
    if verbose:
        print(f"找到 {len(web_results)} 个网页结果和 {len(news_results)} 个新闻结果")
    
    # 3. 并行网页解析
    start_time = time.time()
    start_datetime = datetime.now()
    if verbose:
        print(f"开始时间: {start_datetime.strftime('%H:%M:%S.%f')[:-3]}")
    
    # 收集所有URL
    urls = [i['url'] for i in web_results + news_results]
    if verbose:
        print(f"开始处理 {len(urls)} 个URL...")
    
    # 并行处理所有URL
    results = parse_multiple_pages(urls)
    if verbose:
        for i in results:
            print(len(i[1]))
    
    # 处理结果
    web_text_dict = {}
    total_parse_time = 0.0
    max_parse_time = 0.0
    min_parse_time = float('inf')
    
    for url, text, parse_time in results:
        if not text.strip():  # 跳过空文本
            continue
            
        total_parse_time += parse_time
        max_parse_time = max(max_parse_time, parse_time)
        min_parse_time = min(min_parse_time, parse_time)
        
        # 分块处理
        text_chunks = chunk_split(text)
        for chunk in text_chunks:
            web_text_dict[chunk] = url
    
    end_time = time.time()
    stats['web_parse_time'] = end_time - start_time
    stats['total_parse_time'] = total_parse_time
    stats['max_parse_time'] = max_parse_time
    stats['min_parse_time'] = min_parse_time
    stats['avg_parse_time'] = total_parse_time / len(urls) if urls else 0
    
    if verbose:
        print(f"\n解析统计信息:")
        print(f"URL数量: {len(urls)}")
        print(f"最长处理时间: {max_parse_time:.4f}s")
        print(f"最短处理时间: {min_parse_time:.4f}s")
        print(f"平均处理时间: {stats['avg_parse_time']:.4f}s")
        print(f"并行处理效率提升: {total_parse_time/(end_time-start_time):.1f}x")
    
    # 4. 向量化和相似度搜索
    start_time = time.time()
    text_list = list(web_text_dict.keys())
    if not text_list:  # 如果没有有效的文本，提前返回
        return [], stats
        
    # 向量化所有文本块
    vectors = embed_texts(text_list)
    
    # 向量化查询
    query_vector = embed_text(query)
    
    # 相似度搜索
    similar_indices = faiss_search(query_vector, vectors, k=min(top_k, len(text_list)))
    stats['vector_search_time'] = time.time() - start_time
    
    # 5. 整理结果
    results = []
    for idx in similar_indices:
        text = text_list[idx]
        url = web_text_dict[text]
        results.append({
            'text': text,
            'url': url
        })
    
    if verbose:
        print(f"\n找到 {len(results)} 个相关结果")
        
    return results, stats

# 使用示例
if __name__ == "__main__":
    query = "china destroyer with Australia"
    results, stats = search_pipeline(query, top_k=5, verbose=True)
    
    print("\n搜索结果:")
    for i, result in enumerate(results, 1):
        print(f"\n结果 {i}:")
        print(f"文本: {result['text']}")
        print(f"来源: {result['url']}")
    
    print("\n性能统计:")
    for key, value in stats.items():
        print(f"{key}: {value:.4f}s") 