import unittest
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.cpm_agent import CPMAgent
from utils.config import config_manager

class TestCPMAgent(unittest.TestCase):
    
    def setUp(self):
        # 重置配置管理器，确保每次测试都重新加载配置
        config_manager.configs = {}
        
    def test_agent_initialization(self):
        """测试CPM智能体初始化"""
        try:
            agent = CPMAgent()
            self.assertIsInstance(agent, CPMAgent)
            print("✓ 智能体初始化测试通过")
        except Exception as e:
            self.fail(f"智能体初始化失败: {e}")
    
    def test_config_loading(self):
        """测试配置加载"""
        # 加载配置
        config_manager.load_all_configs()
        self.config = config_manager.configs
        
        self.assertIsNotNone(self.config)
        self.assertIn('agent', self.config)
        self.assertIn('model', self.config)
        self.assertIn('tool', self.config)
        print("✓ 配置加载测试通过")
    
    def test_agent_simple_call(self):
        """测试智能体简单调用流程"""
        try:
            from unittest.mock import patch
            
            # 创建智能体实例
            agent = CPMAgent()
            
            # 使用mock替换模型生成方法，避免实际调用模型
            with patch.object(agent.model, 'generate_text', return_value='测试响应') as mock_generate:
                # 调用run_sync方法
                result = agent.run_sync("测试智能体调用")
                self.assertIsInstance(result, str)
                # 验证生成方法被调用
                mock_generate.assert_called()
            
            print("✓ 智能体简单调用测试通过")
        except Exception as e:
            self.fail(f"智能体简单调用测试失败: {e}")

if __name__ == '__main__':
    unittest.main()
