# langchain-cpm

基于LangChain DeepAgents和AgentCPM模型搭建的智能体系统框架。

## 项目介绍

langchain-cpm是一个基于LangChain DeepAgents和AgentCPM-Explore模型的智能体系统框架，旨在帮助开发者快速构建和部署具有复杂任务处理能力的智能体应用。该框架支持多步骤任务的分解、计划、执行和反思，能够处理各种复杂的自然语言任务。

## 功能特性

- **基于LangChain DeepAgents**：利用LangChain DeepAgents的强大规划和执行能力
- **支持AgentCPM模型**：集成了OpenBMB的AgentCPM-Explore模型，具有强大的文本生成能力
- **灵活的配置系统**：使用YAML格式的配置文件，支持模型、智能体和工具的灵活配置
- **模块化设计**：清晰的代码结构，便于扩展和定制
- **多种工具支持**：内置搜索、文件读取和代码执行等工具
- **提示词管理**：专门的提示词文件夹，支持YAML格式的提示词管理
- **状态管理**：支持智能体状态的持久化和恢复

## 技术栈

- **Python 3.10+**：主要开发语言
- **LangChain**：LLM应用开发框架
- **LangGraph**：DeepAgents的底层图执行和状态管理
- **Transformers**：Hugging Face模型库，用于加载AgentCPM模型
- **PyTorch**：深度学习框架，用于模型推理
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
env\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置环境变量**

复制`.env.example`文件为`.env`，并根据需要修改配置：

```bash
cp .env.example .env
# 使用文本编辑器编辑.env文件
```

## 配置说明

项目使用YAML格式的配置文件，位于`src/config`目录下：

- **model_config.yaml**：模型配置，包括模型名称、路径、参数和量化设置
- **agent_config.yaml**：智能体配置，包括最大步骤数、超时时间、计划策略和反思机制
- **tool_config.yaml**：工具配置，包括启用的工具和工具特定的参数

环境变量可以覆盖配置文件中的设置，主要环境变量包括：

- **HUGGINGFACE_API_KEY**：Hugging Face API密钥
- **MODEL_NAME**：模型名称，默认：`openbmb/AgentCPM-Explore`
- **MODEL_PATH**：本地模型路径（如果使用本地模型）
- **MODEL_MAX_LENGTH**：模型生成的最大长度
- **MODEL_TEMPERATURE**：模型生成的温度参数
- **AGENT_MAX_STEPS**：智能体的最大步骤数
- **AGENT_TIMEOUT**：智能体的超时时间（秒）

## 使用示例

### 基本使用

```python
from src.agents.cpm_agent import cpm_agent
from src.utils.config import config_manager
from src.utils.prompt_utils import prompt_manager

# 加载配置和提示词
config_manager.load_all_configs()
config_manager.merge_with_env()
prompt_manager.load_all_prompts()

# 定义任务
task = "Explain the concept of object-oriented programming in Python"

# 运行智能体
result = cpm_agent.run(task)

# 输出结果
print(result)
```

### 运行示例脚本

项目提供了一个示例脚本，演示智能体的基本使用：

```bash
python examples/basic_usage.py
```

## 项目结构

```
langchain-cpm/
├── src/                     # 源代码目录
│   ├── agents/              # 智能体相关代码
│   │   ├── __init__.py
│   │   └── cpm_agent.py     # AgentCPM智能体实现
│   ├── models/              # 模型相关代码
│   │   ├── __init__.py
│   │   └── cpm_model.py     # AgentCPM模型封装
│   ├── tools/               # 工具相关代码
│   │   ├── __init__.py
│   │   └── cpm_tools.py     # 自定义工具实现
│   ├── utils/               # 工具函数
│   │   ├── __init__.py
│   │   ├── config.py        # 配置管理
│   │   └── prompt_utils.py  # 提示词管理工具
│   ├── prompts/             # 提示词文件夹
│   │   ├── __init__.py
│   │   ├── base_prompt.yaml # 基础提示词
│   │   └── task_prompts/    # 任务特定提示词
│   │       └── research.yaml # 研究任务提示词
│   └── config/              # 配置文件目录
│       ├── __init__.py
│       ├── model_config.yaml # 模型配置
│       ├── agent_config.yaml # 智能体配置
│       └── tool_config.yaml  # 工具配置
├── examples/                # 示例应用
│   └── basic_usage.py       # 基本使用示例
├── .env.example             # 环境变量示例
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

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues：https://github.com/your-username/langchain-cpm/issues
- Email：your-email@example.com

## 致谢

- [LangChain](https://github.com/langchain-ai/langchain)：LLM应用开发框架
- [OpenBMB](https://github.com/OpenBMB)：AgentCPM-Explore模型的开发者
- [Hugging Face](https://huggingface.co/)：提供模型库和工具
