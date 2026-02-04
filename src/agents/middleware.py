# 智能体中间件模块
from langchain.agents.middleware import after_model
from langchain.agents.middleware import AgentState
from langgraph.runtime import Runtime
from langchain_core.messages import AIMessage
import re
import json
from typing import Any

@after_model
def tool_call_extractor_middleware(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """从模型响应中提取 tool_call 标签并转换为标准 tool_calls 格式
    
    Args:
        state: 智能体状态，包含消息历史
        runtime: 运行时对象
        
    Returns:
        更新后的状态，或 None 如果不需要更新
    """
    # 检查状态中是否有消息
    if 'messages' not in state or not state['messages']:
        return None
    
    # 获取最后一条消息（通常是模型的响应）
    last_message = state['messages'][-1]
    
    # 检查是否是 AIMessage
    if not isinstance(last_message, AIMessage):
        return None
    
    # 检查消息内容中是否包含 tool_call 标签
    if not hasattr(last_message, 'content') or '<tool_call>' not in last_message.content:
        return None
    
    # 提取 tool_call 标签中的内容
    tool_call_match = re.search(r'<tool_call>(.*?)</tool_call>', last_message.content, re.DOTALL)
    if not tool_call_match:
        return None
    
    tool_call_content = tool_call_match.group(1).strip()
    
    try:
        # 解析工具调用 JSON
        tool_call_data = json.loads(tool_call_content)
        
        # 检查工具调用格式是否正确
        if 'name' not in tool_call_data or 'arguments' not in tool_call_data:
            return None
        
        # 创建标准的工具调用格式
        import time
        tool_call_id = f"tool_call_{int(time.time() * 1000)}"
        tool_call = {
            'name': tool_call_data['name'],
            'args': tool_call_data['arguments'],
            'id': tool_call_id
        }
        
        # 更新消息的 tool_calls 字段
        last_message.tool_calls = [tool_call]
        
        # 从内容中移除 tool_call 标签
        cleaned_content = re.sub(r'<tool_call>.*?</tool_call>', '', last_message.content, flags=re.DOTALL)
        last_message.content = cleaned_content.strip()
        
        # 返回更新后的状态
        return {
            'messages': state['messages']
        }
        
    except json.JSONDecodeError as e:
        print(f"解析工具调用 JSON 失败: {e}")
        return None
    except Exception as e:
        print(f"处理工具调用时出错: {e}")
        return None
