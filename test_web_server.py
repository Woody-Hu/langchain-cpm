# Web Server测试文件
import pytest
import httpx
from app import app
from fastapi.testclient import TestClient

# 创建测试客户端
client = TestClient(app)

class TestWebServer:
    """Web Server测试类"""

    def test_health_check(self):
        """测试健康检查接口"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "service": "LangChainCPMAgent"}

    def test_root(self):
        """测试根路径接口"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to LangChainCPMAgent API", "version": "1.0.0"}

    def test_chat(self):
        """测试聊天接口"""
        # 测试正常请求
        payload = {"message": "Hello, how are you?"}
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        assert "response" in response.json()
        assert isinstance(response.json()["response"], str)

    def test_chat_empty_message(self):
        """测试聊天接口空消息"""
        # 测试空消息
        payload = {"message": ""}
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        assert "response" in response.json()

    def test_chat_tool_calling(self):
        """测试聊天接口工具调用"""
        # 测试工具调用
        payload = {
            "message": "What's the performance data for Meta/Llama-3-70B-Instruct with vllm on nvidia/h800?"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        assert "response" in response.json()
        assert isinstance(response.json()["response"], str)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
