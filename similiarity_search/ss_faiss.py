import faiss
import numpy as np

def faiss_search(query_vector: np.ndarray, embedding: np.ndarray, k: int = 5) -> list:
    """
    使用FAISS进行相似度搜索
    
    Args:
        query_vector: 查询向量
        embedding: 文本库的向量表示
        k: 返回最相似的k个结果
        
    Returns:
        list: 包含最相似文本索引的列表
    """
    # 获取向量维度
    dim = embedding.shape[1]
    
    # 创建FAISS索引
    index = faiss.IndexFlatL2(dim)
    
    # 确保embedding是numpy数组
    if not isinstance(embedding, np.ndarray):
        if hasattr(embedding, 'device') and str(embedding.device) != 'cpu':
            embedding = embedding.cpu()
        embedding = embedding.numpy()
    
    # 添加文本库向量到索引
    index.add(embedding)
    
    # 确保查询向量是numpy数组
    if not isinstance(query_vector, np.ndarray):
        if hasattr(query_vector, 'device') and str(query_vector.device) != 'cpu':
            query_vector = query_vector.cpu()
        query_vector = query_vector.numpy()
    
    # 确保查询向量是2D数组
    if len(query_vector.shape) == 1:
        query_vector = query_vector.reshape(1, -1)
    
    # 执行搜索
    distances, indices = index.search(query_vector, k=k)
    
    # 获取最相似的文本索引
    top_chunks_idx = [idx for idx in indices[0]]
    
    return top_chunks_idx







    

