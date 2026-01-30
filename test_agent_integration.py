#!/usr/bin/env python3
"""
Integration test for the agent system.
Tests the complete agent workflow including model loading, tool calling, and result generation.
"""

from src.agents.agent import agent
import asyncio
import time

async def test_agent_integration():
    """Test the complete agent integration."""
    print("=" * 60)
    print("Testing Agent Integration")
    print("=" * 60)
    
    try:
        # Test 1: Basic agent initialization
        print("\n1. Testing agent initialization...")
        start_time = time.time()
        
        # Verify agent is a callable function
        if callable(agent):
            print("✓ Agent function is callable")
        else:
            print("✗ Agent is not callable")
            return False
        
        # Test 2: Simple task
        print("\n2. Testing simple task...")
        simple_task = "Hello, how are you?"
        print(f"Task: {simple_task}")
        
        simple_result = await agent(simple_task)
        print(f"Result: {simple_result}")
        
        if simple_result:
            print("✓ Simple task completed successfully")
        else:
            print("✗ Simple task failed: Empty response")
            return False
        
        # Test 3: Tool calling task
        print("\n3. Testing tool calling task...")
        tool_task = "What's the best config for Qwen/Qwen3-235B-A22B with vllm on nvidia/h800?"
        print(f"Task: {tool_task}")
        
        tool_result = await agent(tool_task)
        print(f"Result: {tool_result}")
        
        if tool_result:
            print("✓ Tool calling task completed successfully")
        else:
            print("✗ Tool calling task failed: Empty response")
            return False
        
        # Test 4: Another tool calling task
        print("\n4. Testing another tool calling task...")
        another_task = "What's the performance data for Meta/Llama-3-70B-Instruct with vllm on nvidia/h800?"
        print(f"Task: {another_task}")
        
        another_result = await agent(another_task)
        print(f"Result: {another_result}")
        
        if another_result:
            print("✓ Another tool calling task completed successfully")
        else:
            print("✗ Another tool calling task failed: Empty response")
            return False
        
        end_time = time.time()
        total_time = end_time - start_time
        print(f"\nTotal test time: {total_time:.2f} seconds")
        
        print("\n" + "=" * 60)
        print("All agent integration tests PASSED!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"✗ Error during agent integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_agent_integration())
