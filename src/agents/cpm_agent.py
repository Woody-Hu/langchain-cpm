# 参考 DeepAgents 设计理念实现的 CPM 智能体
# 使用 async/await 异步实现
from src.models.cpm_model import CPMModel
from src.utils.config import config_manager
from src.utils.prompt_utils import prompt_manager
import asyncio

class CPMAgent:
    """AgentCPM agent based on DeepAgents design principles with async/await."""
    
    def __init__(self):
        # 加载所有配置文件
        config_manager.load_all_configs()
        self.config = config_manager.get("agent", {})
        # 在加载配置后创建模型实例
        self.model = CPMModel()
        # 加载所有提示模板
        prompt_manager.load_all_prompts()
        # 获取工具列表
        self.tools = self._get_tools()
        # 初始化内存和其他必要组件
        self.memory = []
        
    def _get_tools(self):
        """获取智能体可用的工具列表"""
        from src.tools.cpm_tools import tools
        return tools.get_tools()
    
    async def run(self, task, config=None):
        """异步运行智能体执行指定任务
        
        Args:
            task: 要执行的任务描述
            config: 可选的配置参数，用于覆盖默认配置
            
        Returns:
            任务执行结果
        """
        if config:
            self.config.update(config)
        
        # 简化实现：直接调用模型生成答案
        # 使用 system 提示模板，而不是 base_prompt
        system_prompt = await self._async_render_prompt("system", task=task)
        return await self._async_generate_text(system_prompt + f"\n\nTask: {task}")
    
    async def _async_render_prompt(self, prompt_name, **kwargs):
        """异步渲染提示模板"""
        # 使用 asyncio.to_thread 包装同步方法，实现异步调用
        return await asyncio.to_thread(
            prompt_manager.render_prompt,
            prompt_name,
            **kwargs
        )
    
    async def _async_generate_text(self, prompt, **kwargs):
        """异步生成文本"""
        # 使用 asyncio.to_thread 包装同步方法，实现异步调用
        return await asyncio.to_thread(
            self.model.generate_text,
            prompt,
            **kwargs
        )
    
    def get_agent_info(self):
        """获取智能体信息"""
        return {
            "agent_type": "CPMAgent",
            "model": self.model.get_model_info(),
            "tools": [tool.name for tool in self.tools],
            "config": self.config
        }
    
    def run_sync(self, task, config=None):
        """同步运行智能体的包装器，保持向后兼容"""
        return asyncio.run(self.run(task, config))

# 创建全局实例
cpm_agent = CPMAgent()
