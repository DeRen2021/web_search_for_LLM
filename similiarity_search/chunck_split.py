import re
from typing import List

def split_text_into_words(text: str) -> List[str]:
    """
    将文本分割成英文单词
    
    Args:
        text: 要分割的文本
        
    Returns:
        单词列表
    """
    # 清理文本：标准化空白字符
    text = ' '.join(text.split())
    
    # 使用正则表达式分割英文单词
    # 1. 保留完整的英文单词（包括带连字符的单词）
    # 2. 保留数字
    # 3. 保留基本标点符号
    words = []
    for word in text.split():
        # 移除单词前后的标点符号
        word = word.strip('.,!?;:()[]{}""\'')
        if word:
            words.append(word)
    
    return words

def chunk_split(text: str, chunk_size: int = 256, overlap: int = 50) -> List[str]:
    """
    将文本分割成固定单词数量的块，可以设置重叠部分
    
    Args:
        text: 要分割的文本
        chunk_size: 每个块的单词数量
        overlap: 块之间的重叠单词数量
        
    Returns:
        分割后的文本块列表
    """
    # 分词
    words = split_text_into_words(text)
    
    # 如果单词数量小于块大小，直接返回
    if len(words) <= chunk_size:
        return [' '.join(words)] if words else []
    
    chunks = []
    start = 0
    
    while start < len(words):
        # 确定当前块的结束位置
        end = min(start + chunk_size, len(words))
        
        # 提取当前块的单词并组合成文本
        chunk = ' '.join(words[start:end])
        if chunk:  # 只添加非空的块
            chunks.append(chunk)
        
        # 更新起始位置，考虑重叠
        start = end - overlap if end < len(words) else len(words)
    
    return chunks


