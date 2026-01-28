import os
import subprocess
from langchain.tools import tool
from src.utils.config import config_manager

class CPMTools:
    """Toolset for AgentCPM agent."""
    
    def __init__(self):
        self.config = config_manager.get("tools", {})
    
    @tool
    def search(self, query: str, max_results: int = 5) -> str:
        """Search the web for information about a given query.
        
        Args:
            query: The search query.
            max_results: The maximum number of results to return.
        
        Returns:
            A string containing the search results.
        """
        # 空实现，仅返回提示信息
        return f"Search results for '{query}' (showing {max_results} results):\n\n" + """
        # 这是一个空实现，实际搜索功能尚未实现
        # 1. 搜索结果 1 - 示例结果
        # 2. 搜索结果 2 - 示例结果
        # 3. 搜索结果 3 - 示例结果
        # 4. 搜索结果 4 - 示例结果
        # 5. 搜索结果 5 - 示例结果
        """
    
    @tool
    def file_reader(self, file_path: str) -> str:
        """Read the content of a file.
        
        Args:
            file_path: The path to the file to read.
        
        Returns:
            The content of the file as a string.
        """
        # Check if the file exists
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
        
        # Check file size
        file_size = os.path.getsize(file_path)
        max_size = self.config.get("file_reader", {}).get("max_file_size", 1048576)  # 1MB
        if file_size > max_size:
            return f"Error: File '{file_path}' is too large. Maximum size is {max_size} bytes."
        
        # Check file type
        supported_types = self.config.get("file_reader", {}).get("supported_types", [".txt", ".md", ".json", ".yaml", ".py"])
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in supported_types:
            return f"Error: File type '{file_ext}' is not supported. Supported types: {', '.join(supported_types)}."
        
        # Read the file content
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"
    
    @tool
    def code_executor(self, code: str, language: str = "python") -> str:
        """Execute code and return the output.
        
        Args:
            code: The code to execute.
            language: The programming language of the code.
        
        Returns:
            The output of the code execution.
        """
        # Check if the language is supported
        supported_languages = self.config.get("code_executor", {}).get("supported_languages", ["python", "javascript", "bash"])
        if language not in supported_languages:
            return f"Error: Language '{language}' is not supported. Supported languages: {', '.join(supported_languages)}."
        
        # Execute the code
        try:
            if language == "python":
                result = subprocess.run(
                    ["python", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=self.config.get("code_executor", {}).get("max_execution_time", 30)
                )
            elif language == "javascript":
                result = subprocess.run(
                    ["node", "-e", code],
                    capture_output=True,
                    text=True,
                    timeout=self.config.get("code_executor", {}).get("max_execution_time", 30)
                )
            elif language == "bash":
                result = subprocess.run(
                    ["bash", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=self.config.get("code_executor", {}).get("max_execution_time", 30)
                )
            else:
                return f"Error: Language '{language}' is not supported."
            
            # Format the output
            output = ""
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n\n"
            output += f"Return Code: {result.returncode}"
            
            return output
        except subprocess.TimeoutExpired:
            return f"Error: Code execution timed out after {self.config.get('code_executor', {}).get('max_execution_time', 30)} seconds."
        except Exception as e:
            return f"Error executing code: {str(e)}"
    
    def get_tools(self):
        """Get the list of enabled tools."""
        enabled_tools = self.config.get("enabled", ["search", "file_reader", "code_executor"])
        tools = []
        
        if "search" in enabled_tools:
            tools.append(self.search)
        if "file_reader" in enabled_tools:
            tools.append(self.file_reader)
        if "code_executor" in enabled_tools:
            tools.append(self.code_executor)
        
        return tools

# Create a global instance of CPMTools
tools = CPMTools()
