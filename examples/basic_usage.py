#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic usage example for the AgentCPM agent.

This example demonstrates how to initialize the agent, define a task, and run the agent to get results.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.cpm_agent import cpm_agent
from src.utils.config import config_manager
from src.utils.prompt_utils import prompt_manager
from src.models.cpm_model import cpm_model

def main():
    """Main function to run the basic usage example."""
    print("=" * 60)
    print("AgentCPM Basic Usage Example")
    print("=" * 60)
    
    # Load all configurations
    config_manager.load_all_configs()
    config_manager.merge_with_env()
    
    # Load all prompts
    prompt_manager.load_all_prompts()
    
    # Print model information
    print("\n1. Model Information:")
    print("-" * 30)
    try:
        model_info = cpm_model.get_model_info()
        for key, value in model_info.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error getting model info: {e}")
    
    # Define a simple task
    task = "Explain the concept of object-oriented programming in Python, including classes, objects, inheritance, and polymorphism."
    
    print("\n2. Task:")
    print("-" * 30)
    print(task)
    
    # Run the agent
    print("\n3. Running Agent...")
    print("-" * 30)
    try:
        result = cpm_agent.run(task)
        
        print("\n4. Result:")
        print("-" * 30)
        print(result)
    except Exception as e:
        print(f"Error running agent: {e}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
