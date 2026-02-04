# 使用 LangChain 标准方法实现的智能体
from langchain.agents import create_agent
from src.tools.cpm_tools import get_performance_data
from src.models.agent_model import llm
from src.utils.prompt_utils import prompt_manager
from src.utils.config import config_manager
from src.agents.middleware import tool_call_extractor_middleware
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
llm.bind_tools(tools)
# 创建智能体
agent_instance = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    middleware=[tool_call_extractor_middleware]
)

# 智能体运行函数
async def run(task, config=None):
    """运行智能体执行指定任务
    
    Args:
        task: 要执行的任务描述
        config: 可选的配置参数，用于覆盖默认配置
        
    Returns:
        格式化的任务执行结果，包含性能数据和简要概括
    """
    # 使用智能体处理任务
    result = await agent_instance.ainvoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    # 打印详细信息，便于调试
    print(f"Result type: {type(result)}")
    print(f"Result content: {result}")
    
    # 提取性能数据和生成简要概括
    performance_data = []
    summary_message = ""
    
    # 检查是否有工具调用和结果
    if isinstance(result, dict) and 'messages' in result:
        for i, msg in enumerate(result['messages']):
            print(f"Message {i} type: {type(msg)}")
            print(f"Message {i} content: {msg}")
            
            # 检查是否是 ToolMessage，提取性能数据
            if hasattr(msg, 'name') and msg.name == 'get_performance_data':
                print(f"Found ToolMessage with performance data at index {i}")
                try:
                    import json
                    # 解析工具返回的性能数据
                    tool_data = json.loads(msg.content)
                    if isinstance(tool_data, list):
                        performance_data.extend(tool_data)
                except Exception as e:
                    print(f"Error parsing tool data: {e}")
    
    # 生成简要概括
    if performance_data:
        # 基于性能数据生成简要概括
        first_data = performance_data[0]
        model_name = first_data.get('model_name', 'Unknown')
        engine_name = first_data.get('engine_name', 'Unknown')
        device_type = first_data.get('device_type', 'Unknown')
        throughput = first_data.get('throughput', 0)
        
        summary_message = f"找到 {len(performance_data)} 个关于 {model_name} 在 {device_type} 上使用 {engine_name} 引擎的性能配置，最高吞吐量为 {throughput:.2f} tokens/sec"
    else:
        summary_message = "未找到性能数据"
    
    # 构建格式化返回结果
    formatted_result = {
        "message": summary_message,
        "performance_data": performance_data
    }
    
    # 处理不同的返回格式
    if isinstance(result, dict):
        if 'messages' in result and result['messages']:
            last_message = result['messages'][-1]
            if hasattr(last_message, 'content'):
                return formatted_result
            elif isinstance(last_message, dict) and 'content' in last_message:
                return formatted_result
        elif 'output' in result:
            return formatted_result
        elif 'structured_response' in result:
            return formatted_result
    
    # 返回格式化结果作为后备
    return formatted_result

# 全局导出
agent = run