# LangChainCPMAgent

基于LangChain DeepAgents和MiniCPM4-0.5B模型搭建的智能体系统框架。

## 项目介绍

LangChainCPMAgent是一个基于LangChain DeepAgents和OpenBMB的MiniCPM4-0.5B模型的智能体系统框架，专为性能数据查询和配置优化而设计。该框架利用DeepAgents的强大规划和执行能力，结合MiniCPM4-0.5B模型的优秀文本生成能力，为用户提供高质量的性能配置建议。

## 功能特性

- **基于LangChain DeepAgents**：利用DeepAgents的强大规划和执行能力
- **支持本地MiniCPM4-0.5B模型**：集成了OpenBMB的MiniCPM4-0.5B模型，使用本地推理，无需外部API密钥
- **异步支持**：完全异步的实现，适合FastAPI等异步框架
- **单例模型加载**：模型只加载一次，节省资源，提高性能
- **性能数据工具**：内置性能数据查询工具，提供最佳配置建议
- **灵活的配置系统**：使用YAML格式的配置文件，支持模型和工具的灵活配置
- **模块化设计**：清晰的代码结构，便于扩展和定制

## 技术栈

- **Python 3.10+**：主要开发语言
- **LangChain**：LLM应用开发框架
- **llama-cpp-python**：llama.cpp的Python绑定，用于模型推理
- **ModelScope**：模型下载和管理
- **PyYAML**：YAML配置文件解析
- **python-dotenv**：环境变量管理

## 安装方法

1. **克隆仓库**

```bash
git clone https://github.com/your-username/langchain-cpm.git
cd langchain-cpm
```

2. **创建虚拟环境**

```bash
# 使用venv创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置说明**

项目使用YAML格式的配置文件，位于`src/config`目录下：

- **model_config.yaml**：模型配置，包括模型名称、路径、参数和量化设置

## 使用示例

### 基本使用

```python
from src.agents.agent import agent

# 定义任务
task = "What's the best config for Qwen/Qwen3-235B-A22B with vllm on nvidia/h800?"

# 异步运行智能体
import asyncio
result = asyncio.run(agent(task))

# 输出结果
print(result)
```

### Web Server 使用

LangChainCPMAgent提供了基于FastAPI的Web Server，支持HTTP API接口调用。

#### 启动Web Server

```bash
# 直接运行
python app.py

# 或者使用uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
```

#### API接口说明

- **健康检查接口**：`GET /health`
  - 响应示例：
  ```json
  {"status": "healthy", "service": "LangChainCPMAgent"}
  ```

- **聊天接口**：`POST /chat`
  - 请求体：
  ```json
  {"message": "What's the best config for Qwen/Qwen3-235B-A22B with vllm on nvidia/h800?"}
  ```
  - 响应示例：
  ```json
  {"response": "为了找到Qwen/Qwen3-235B-A22B的最佳配置，我们需要..."}
  ```

- **根路径**：`GET /`
  - 响应示例：
  ```json
  {"message": "Welcome to LangChainCPMAgent API", "version": "1.0.0"}
  ```

#### 使用示例

**使用curl**：

```bash
# 健康检查
curl http://localhost:8000/health

# 聊天
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What's the best config for Qwen/Qwen3-235B-A22B with vllm on nvidia/h800?"}'
```

**使用Python**：

```python
import requests

# 健康检查
response = requests.get("http://localhost:8000/health")
print(response.json())

# 聊天
payload = {"message": "What's the best config for Qwen/Qwen3-235B-A22B with vllm on nvidia/h800?"}
response = requests.post("http://localhost:8000/chat", json=payload)
print(response.json())
```

#### Docker部署

```bash
# 构建镜像
docker build -t langchain-cpm-agent .

# 运行容器
docker run -p 8000:8000 langchain-cpm-agent
```


## 项目结构

```
langchain-cpm/
├── src/                     # 源代码目录
│   ├── agents/              # 智能体相关代码
│   │   ├── __init__.py
│   │   └── agent.py         # Agent智能体实现
│   ├── models/              # 模型相关代码
│   │   ├── __init__.py
│   │   └── agent_model.py   # MiniCPM4-0.5B模型封装和LangChain兼容包装器
│   ├── tools/               # 工具相关代码
│   │   ├── __init__.py
│   │   └── cpm_tools.py     # 性能数据工具实现
│   ├── utils/               # 工具函数
│   │   ├── __init__.py
│   │   ├── config.py        # 配置管理
│   │   └── prompt_utils.py  # 提示词管理
│   ├── config/              # 配置文件目录
│   │   ├── __init__.py
│   │   └── model_config.yaml # 模型配置
│   └── prompts/             # 提示词目录
│       ├── __init__.py
│       └── system_prompt.txt # 系统提示词
├── app.py                   # FastAPI Web Server
├── test_agent_integration.py # 集成测试
├── test_web_server.py       # Web Server测试
├── Dockerfile               # Docker构建文件
├── requirements.txt         # 项目依赖
└── README.md                # 项目说明
```

## 贡献指南

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 致谢

- [LangChain](https://github.com/langchain-ai/langchain)：LLM应用开发框架
- [OpenBMB](https://github.com/OpenBMB)：AgentCPM-Explore模型的开发者
- [Hugging Face](https://huggingface.co/)：提供模型库和工具
