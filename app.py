# FastAPI web server for LangChainCPMAgent
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.agent import agent
import asyncio

# 创建FastAPI应用实例
app = FastAPI(
    title="LangChainCPMAgent API",
    description="智能体系统API接口",
    version="1.0.0"
)

# 请求模型
class ChatRequest(BaseModel):
    message: str

# 响应模型
class ChatResponse(BaseModel):
    response: str

# Health check接口
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "LangChainCPMAgent"}

# Chat接口
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天接口，接收消息并返回智能体的响应"""
    try:
        # 调用智能体处理消息
        response = await agent(request.message)
        # 返回响应
        return ChatResponse(response=response)
    except Exception as e:
        # 处理异常
        raise HTTPException(status_code=500, detail=f"处理消息时发生错误: {str(e)}")

# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {"message": "Welcome to LangChainCPMAgent API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
