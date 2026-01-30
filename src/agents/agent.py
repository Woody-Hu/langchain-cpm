# 使用 LangChain 标准方法实现的智能体
from langchain.agents import create_agent
from src.tools.cpm_tools import get_performance_data
from src.models.agent_model import llm
from src.utils.prompt_utils import prompt_manager
from src.utils.config import config_manager
import os

# 加载配置
config_manager.load_all_configs()
config_manager.merge_with_env()

# 加载提示词
prompt_manager.load_all_prompts()

# 定义工具列表
tools = [get_performance_data]

# 加载系统提示词
def load_system_prompt():
    """从外部文件加载系统提示词"""
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'system_prompt.txt')
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error loading system prompt: {e}")
        # 返回默认提示词作为后备
        return "你是一个性能数据专家。你的任务是帮助用户找到模型、引擎和设备类型的最佳配置。"

# 加载系统提示词
system_prompt = load_system_prompt()

# 创建智能体
agent_instance = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)

# 智能体运行函数
async def run(task, config=None):
    """运行智能体执行指定任务
    
    Args:
        task: 要执行的任务描述
        config: 可选的配置参数，用于覆盖默认配置
        
    Returns:
        任务执行结果
    """
    # 使用智能体处理任务
    result = await agent_instance.ainvoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    # 处理不同的返回格式
    if isinstance(result, dict):
        if 'messages' in result and result['messages']:
            last_message = result['messages'][-1]
            if hasattr(last_message, 'content'):
                return last_message.content
            elif isinstance(last_message, dict) and 'content' in last_message:
                return last_message['content']
        elif 'output' in result:
            return result['output']
        elif 'structured_response' in result:
            return str(result['structured_response'])
    
    # 返回原始结果作为后备
    return str(result)

# 全局导出
agent = run