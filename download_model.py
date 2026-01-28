from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download
import yaml
import os

# 读取模型配置
def load_model_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 下载模型
def download_model(config):
    model_name = config['model']['name']
    cache_dir = config['model']['cache_dir']
    
    if not cache_dir:
        cache_dir = os.path.join(os.getcwd(), '.cache')
    
    print(f"开始下载模型: {model_name}")
    print(f"缓存目录: {cache_dir}")
    
    # 使用snapshot_download下载完整模型
    snapshot_download(
        repo_id=model_name,
        cache_dir=cache_dir,
        ignore_patterns=["*.bin", "*.pt"]  # 不下载大文件，仅下载配置和tokenizer
    )
    
    # 下载tokenizer
    print("\n下载tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=cache_dir
    )
    
    print("\n模型和tokenizer下载完成!")

if __name__ == "__main__":
    config_path = os.path.join("src", "config", "model_config.yaml")
    config = load_model_config(config_path)
    download_model(config)
