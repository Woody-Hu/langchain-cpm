import os
from src.utils.config import config_manager
from modelscope.hub.snapshot_download import snapshot_download
from langchain_community.chat_models import ChatLlamaCpp


# Singleton instance for ChatLlamaCpp
_chat_llm_instance = None


def _download_model():
    """Download model from ModelScope with GGUF versions filtering."""
    # Get model configuration
    config = config_manager.get("model", {})
    model_name = config.get("name", "DevQuasar/openbmb.MiniCPM4-0.5B-GGUF")
    local_path = config.get("path", "")
    cache_dir = config.get("cache_dir", "./models")
    
    # Ensure cache directories exist
    os.makedirs(cache_dir, exist_ok=True)
    
    # Get GGUF versions to keep from config (guaranteed to have value)
    gguf_versions = config.get("download", {}).get("gguf_versions", [])
    
    if local_path and os.path.exists(local_path):
        # Use local path if provided and exists
        print(f"Using local model path: {local_path}")
        model_path = local_path
        print(f"GGUF versions to keep: {gguf_versions}")
        
        # Assume local path only contains the desired GGUF version
        # No need to filter files for local paths
    else:
        print(f"GGUF versions to download: {gguf_versions}")
        
        # Create allow patterns for GGUF versions filtering
        # Create patterns to match specified GGUF versions
        allow_patterns = []
        # Add patterns for specified GGUF versions
        for version in gguf_versions:
            # Add both lowercase and uppercase patterns to ensure matching
            allow_patterns.append(f"*{version.lower()}*.gguf")
            allow_patterns.append(f"*{version.upper()}*.gguf")
        print(f"Created allow patterns: {allow_patterns}")
        
        # Download model with GGUF versions filtering
        print(f"Downloading model from ModelScope: {model_name}")
        model_path = snapshot_download(
            model_name,
            cache_dir=cache_dir,
            revision="master",
            allow_patterns=allow_patterns
        )
        print(f"Model downloaded to: {model_path}")
        print(f"GGUF versions to keep: {gguf_versions}")
    
    return model_path


def _find_gguf_file(directory, versions):
    """Find GGUF model file in the directory."""
    print(f"Searching for GGUF files in: {directory}")
    print(f"Looking for versions: {versions}")
    
    # Print all files in the directory
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
            print(f"Found file: {file_path}")
    
    # Try to find any GGUF file regardless of version
    for file_path in all_files:
        if file_path.endswith('.gguf'):
            print(f"Found GGUF file: {file_path}")
            return file_path
    
    # Try to find any file that might be a model
    for file_path in all_files:
        if any(ext in file_path.lower() for ext in ['.bin', '.pth', '.pt', '.onnx']):
            print(f"Found potential model file: {file_path}")
            return file_path
    
    return None


def get_chat_llm():
    """Get or create the ChatLlamaCpp instance."""
    global _chat_llm_instance
    
    if _chat_llm_instance:
        return _chat_llm_instance
    
    # Get model configuration
    config = config_manager.get("model", {})
    model_params = config.get("params", {})
    gguf_versions = config.get("download", {}).get("gguf_versions", [])
    
    # Download model if needed
    model_path = _download_model()
    
    # Find GGUF model file (gguf_versions is guaranteed to have value)
    gguf_model_file = _find_gguf_file(model_path, gguf_versions)
    if gguf_model_file:
        print(f"Found specified GGUF model file: {gguf_model_file}")
    else:
        raise Exception(f"No specified GGUF model file found in: {model_path}")
    
    print(f"Using GGUF model file: {gguf_model_file}")
    
    # Create ChatLlamaCpp instance
    llm = ChatLlamaCpp(
        model_path=gguf_model_file,
        temperature=model_params.get("temperature", 0.7),
        max_tokens=model_params.get("max_length", 2048),
        top_p=model_params.get("top_p", 0.95),
        n_ctx=model_params.get("max_length", 2048),
        n_gpu_layers=-1,  # Use all GPU layers if available
        verbose=model_params.get("verbose", False),
    )
    
    # Store singleton instance
    _chat_llm_instance = llm
    print(f"ChatLlamaCpp instance created successfully!")
    
    return llm


# Main export: ChatLlamaCpp instance ready for LangChain agent
llm = get_chat_llm()
