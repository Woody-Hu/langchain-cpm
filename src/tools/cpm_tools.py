from langchain.tools import tool

@tool
def get_performance_data(model_name: str, engine_name: str, device_type: str) -> list:
    """获取指定模型、引擎和设备类型的性能数据。
    
    Args:
        model_name: 模型的完整名称，如 "Qwen/Qwen3-235B-A22B" 或 "Meta/Llama-3-70B-Instruct"
        engine_name: 引擎名称，如 "vllm" 或 "tensorrt-llm"
        device_type: 设备类型，如 "nvidia/h800" 或 "nvidia/h100"
    
    Returns:
        匹配输入参数的性能配置列表。
    """
    # Mock performance data with various configurations
    mock_data = [
        {
            "id": 1,
            "model_name": "Qwen/Qwen3-235B-A22B",
            "engine_name": "vllm",
            "device_type": "nvidia/h800",
            "node_num": 1,
            "device_per_node": 8,
            "scenario": "",
            "dtype": "bfloat16",
            "quantization": "",
            "gpu_memory_utilization": 0.9,
            "data_parallel_size": 0,
            "pipeline_parallel_size": 0,
            "tensor_parallel_size": 8,
            "enable_expert_parallel": False,
            "enable_chunked_prefill": False,
            "ttft": 476.1,
            "tpot": 20.2,
            "qps": 0.47,
            "throughput": 968.73
        },
        {
            "id": 2,
            "model_name": "Qwen/Qwen3-235B-A22B",
            "engine_name": "vllm",
            "device_type": "nvidia/h100",
            "node_num": 1,
            "device_per_node": 8,
            "scenario": "",
            "dtype": "bfloat16",
            "quantization": "",
            "gpu_memory_utilization": 0.9,
            "data_parallel_size": 0,
            "pipeline_parallel_size": 0,
            "tensor_parallel_size": 8,
            "enable_expert_parallel": False,
            "enable_chunked_prefill": True,
            "ttft": 380.5,
            "tpot": 15.3,
            "qps": 0.62,
            "throughput": 1250.45
        },
        {
            "id": 3,
            "model_name": "Qwen/Qwen3-72B-A22B",
            "engine_name": "vllm",
            "device_type": "nvidia/h800",
            "node_num": 1,
            "device_per_node": 4,
            "scenario": "",
            "dtype": "bfloat16",
            "quantization": "",
            "gpu_memory_utilization": 0.9,
            "data_parallel_size": 0,
            "pipeline_parallel_size": 0,
            "tensor_parallel_size": 4,
            "enable_expert_parallel": False,
            "enable_chunked_prefill": False,
            "ttft": 210.3,
            "tpot": 8.7,
            "qps": 1.15,
            "throughput": 1850.22
        },
        {
            "id": 4,
            "model_name": "Meta/Llama-3-70B-Instruct",
            "engine_name": "vllm",
            "device_type": "nvidia/h800",
            "node_num": 1,
            "device_per_node": 4,
            "scenario": "",
            "dtype": "bfloat16",
            "quantization": "",
            "gpu_memory_utilization": 0.9,
            "data_parallel_size": 0,
            "pipeline_parallel_size": 0,
            "tensor_parallel_size": 4,
            "enable_expert_parallel": False,
            "enable_chunked_prefill": False,
            "ttft": 195.7,
            "tpot": 7.9,
            "qps": 1.26,
            "throughput": 1980.56
        },
        {
            "id": 5,
            "model_name": "Qwen/Qwen3-235B-A22B",
            "engine_name": "tensorrt-llm",
            "device_type": "nvidia/h800",
            "node_num": 1,
            "device_per_node": 8,
            "scenario": "",
            "dtype": "bfloat16",
            "quantization": "",
            "gpu_memory_utilization": 0.9,
            "data_parallel_size": 0,
            "pipeline_parallel_size": 0,
            "tensor_parallel_size": 8,
            "enable_expert_parallel": False,
            "enable_chunked_prefill": False,
            "ttft": 420.8,
            "tpot": 18.5,
            "qps": 0.52,
            "throughput": 1050.34
        }
    ]
    
    # Filter data by input parameters
    filtered_data = [
        item for item in mock_data
        if item["model_name"] == model_name and
           item["engine_name"] == engine_name and
           item["device_type"] == device_type
    ]
    
    return filtered_data
