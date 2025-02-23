# Web Search Pipeline / 网页搜索管道

[English](#english) | [中文](#chinese)

## English

### Overview
This project implements a web search pipeline that combines query expansion, web search, content parsing, and semantic similarity search. It's designed to provide more contextually relevant search results by processing and analyzing web content.

### ⚠️ Current Limitations
1. **Query Expansion Limitations**:
   - The OpenAI-based query expansion might misinterpret user intentions
   - Limited by training data cutoff (e.g., might miss recent events)
   - Example: When searching for "destroyer Australia 2025", it might return 2023 events instead

2. **Performance Issues**:
   - Web page parsing is relatively slow (5-7 seconds)
   - Parallel processing could be optimized
   - Memory usage needs optimization for large-scale searches

3. **Robustness Concerns**:
   - Limited error handling and recovery
   - Needs more comprehensive testing
   - No rate limiting or request throttling

### Project Structure
```
.
├── api_server.py           # FastAPI server implementation
├── search_pipeline.py      # Main search pipeline logic
├── query_expand/          # Query expansion using OpenAI
├── brave_search/          # Brave Search API integration
├── web_page_parse/        # Web page content extraction
├── similiarity_search/    # FAISS-based similarity search
└── config/               # Configuration files
```

### Components
1. **Query Expansion** (`query_expand/`)
   - Expands search queries using OpenAI's GPT models
   - Helps in understanding user intent

2. **Web Search** (`brave_search/`)
   - Integrates with Brave Search API
   - Retrieves relevant web pages and news articles

3. **Content Parsing** (`web_page_parse/`)
   - Asynchronous web page content extraction
   - Uses trafilatura for content cleaning

4. **Similarity Search** (`similiarity_search/`)
   - FAISS-based vector similarity search
   - Text chunking and embedding

### API Endpoints
- `GET /search`: Main search endpoint
- `GET /health`: Health check endpoint

### Future Improvements
1. **Query Expansion**:
   - Implement custom query expansion logic
   - Add time-aware query processing
   - Support multiple expansion strategies

2. **Performance**:
   - Optimize web page parsing
   - Implement caching
   - Add request pooling

3. **Robustness**:
   - Add comprehensive error handling
   - Implement retry mechanisms
   - Add monitoring and logging

4. **Testing**:
   - Add unit tests
   - Add integration tests
   - Add performance benchmarks

### Installation
```bash
# Clone the repository
git clone [repository-url]

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the API server
python api_server.py
```

## Chinese

### 概述
本项目实现了一个网页搜索管道，结合了查询扩展、网页搜索、内容解析和语义相似度搜索。它旨在通过处理和分析网页内容来提供更具上下文相关性的搜索结果。

### ⚠️ 当前限制
1. **查询扩展限制**：
   - 基于OpenAI的查询扩展可能误解用户意图
   - 受限于训练数据截止日期（例如，可能遗漏最近事件）
   - 示例：搜索"destroyer Australia 2025"时可能返回2023年的事件

2. **性能问题**：
   - 网页解析相对较慢（5-7秒）
   - 并行处理可以优化
   - 大规模搜索时的内存使用需要优化

3. **健壮性问题**：
   - 错误处理和恢复机制有限
   - 需要更全面的测试
   - 缺少速率限制和请求节流

### 项目结构
```
.
├── api_server.py           # FastAPI服务器实现
├── search_pipeline.py      # 主搜索管道逻辑
├── query_expand/          # 使用OpenAI的查询扩展
├── brave_search/          # Brave搜索API集成
├── web_page_parse/        # 网页内容提取
├── similiarity_search/    # 基于FAISS的相似度搜索
└── config/               # 配置文件
```

### 组件
1. **查询扩展** (`query_expand/`)
   - 使用OpenAI的GPT模型扩展搜索查询
   - 帮助理解用户意图

2. **网页搜索** (`brave_search/`)
   - 集成Brave搜索API
   - 检索相关网页和新闻文章

3. **内容解析** (`web_page_parse/`)
   - 异步网页内容提取
   - 使用trafilatura进行内容清理

4. **相似度搜索** (`similiarity_search/`)
   - 基于FAISS的向量相似度搜索
   - 文本分块和嵌入

### API端点
- `GET /search`: 主搜索端点
- `GET /health`: 健康检查端点

### 未来改进
1. **查询扩展**：
   - 实现自定义查询扩展逻辑
   - 添加时间感知查询处理
   - 支持多种扩展策略

2. **性能**：
   - 优化网页解析
   - 实现缓存
   - 添加请求池

3. **健壮性**：
   - 添加全面的错误处理
   - 实现重试机制
   - 添加监控和日志记录

4. **测试**：
   - 添加单元测试
   - 添加集成测试
   - 添加性能基准测试

### 安装
```bash
# 克隆仓库
git clone [repository-url]

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env
# 编辑.env文件，添加你的API密钥

# 运行API服务器
python api_server.py
``` 