from typing import List, Dict, Tuple
import time
from datetime import datetime

from query_expand.qe_openai import expand_query
from brave_search.brave_search_function import search_and_parse
from web_page_parse.parse_web_function import parse_multiple_pages
from similiarity_search.chunck_split import chunk_split
from similiarity_search.ss_aml import embed_texts, embed_text
from similiarity_search.ss_faiss import faiss_search

def search_pipeline(
    query: str,
    top_k: int = 5,
    chunk_size: int = 256,
    chunk_overlap: int = 50,
    verbose: bool = True
) -> Tuple[List[Dict], Dict[str, float]]:
    """
    完整的搜索管道，包括查询扩展、网页搜索、并行网页解析、向量化和相似度搜索
    
    Args:
        query: 原始查询文本
        top_k: 返回最相似的结果数量
        chunk_size: 文本分块大小
        chunk_overlap: 文本分块重叠大小
        verbose: 是否打印详细信息
        
    Returns:
        Tuple[List[Dict], Dict[str, float]]: 
            - 包含相似文本和对应URL的结果列表
            - 包含各个阶段耗时的统计信息
    """
    stats = {}
    
    # 1. 查询扩展
    start_time = time.time()
    expanded_query = expand_query(query)
    stats['query_expansion_time'] = time.time() - start_time
    if verbose:
        print(f"扩展后的查询: {expanded_query}")
    
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
    
    # 处理结果
    web_text_dict = {}
    total_parse_time = 0.0
    max_parse_time = 0.0
    min_parse_time = float('inf')
    total_chunks = 0
    
    for url, text, parse_time in results:
        if not text or not text.strip():  # 跳过空文本
            continue
            
        total_parse_time += parse_time
        max_parse_time = max(max_parse_time, parse_time)
        min_parse_time = min(min_parse_time, parse_time)
        
        # 分块处理
        try:
            text_chunks = chunk_split(text, chunk_size=chunk_size, overlap=chunk_overlap)
            total_chunks += len(text_chunks)
            for chunk in text_chunks:
                if chunk and chunk.strip():  # 只保存非空块
                    web_text_dict[chunk] = url
        except Exception as e:
            if verbose:
                print(f"处理URL时出错 {url}: {str(e)}")
            continue
    
    end_time = time.time()
    stats['web_parse_time'] = end_time - start_time
    stats['total_parse_time'] = total_parse_time
    stats['max_parse_time'] = max_parse_time
    stats['min_parse_time'] = min_parse_time
    stats['avg_parse_time'] = total_parse_time / len(urls) if urls else 0
    stats['total_chunks'] = total_chunks
    
    if verbose:
        print(f"\n解析统计信息:")
        print(f"URL数量: {len(urls)}")
        print(f"总文本块数: {total_chunks}")
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
            'url': url,
            'length': len(text)  # 添加文本长度信息
        })
    
    if verbose:
        print(f"\n找到 {len(results)} 个相关结果")
        for i, result in enumerate(results, 1):
            print(f"\n结果 {i} (长度: {result['length']}):")
            print(f"文本: {result['text'][:200]}...")
            print(f"来源: {result['url']}")
        
    return results, stats

# 使用示例
if __name__ == "__main__":
    query = "What caused Silicon Valley Bank to collapse?"
    results, stats = search_pipeline(
        query,
        top_k=5,
        chunk_size=256,
        chunk_overlap=50,
        verbose=True
    )
    
    print("\n性能统计:")
    for key, value in stats.items():
        if isinstance(value, (int, float)):
            print(f"{key}: {value:.4f}s" if key.endswith('time') else f"{key}: {value}") 