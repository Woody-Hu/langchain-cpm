import torch
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, logging
from huggingface_hub import snapshot_download
from src.utils.config import config_manager

# Enable detailed logging for model downloading
logging.set_verbosity_info()

class CPMModel:
    """AgentCPM model wrapper for text generation."""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.config = config_manager.get("model", {})
        self.device = self._get_device()
        self.cache_dir = self._get_cache_dir()
        
    def _get_device(self):
        """Get the appropriate device for model inference."""
        device = self.config.get("device", "auto")
        
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        else:
            return device
    
    def _get_cache_dir(self):
        """Get the cache directory for storing model weights."""
        # Priority: 1. Environment variable, 2. Config file, 3. Default
        cache_dir = os.getenv("HF_HOME")
        if not cache_dir:
            cache_dir = self.config.get("cache_dir")
        if not cache_dir:
            cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
        return cache_dir
    
    def _check_model_exists(self, model_name_or_path):
        """Check if the model already exists locally."""
        if not model_name_or_path:
            return False
        
        # If it's a local path, check if it exists
        if os.path.exists(model_name_or_path):
            return True
        
        # If it's a model name, check if it's in the cache
        try:
            # Check if the model is cached
            from huggingface_hub import model_info
            model_info(model_name_or_path)
            # Try to get the local path
            local_path = os.path.join(self.cache_dir, f"models--{model_name_or_path.replace('/', '--')}")
            return os.path.exists(local_path)
        except Exception:
            return False
    
    def download_model(self, model_name_or_path):
        """Download the model weights if they don't exist locally."""
        if self._check_model_exists(model_name_or_path):
            print(f"Model '{model_name_or_path}' already exists locally, skipping download.")
            return
        
        print(f"Downloading model '{model_name_or_path}' to cache directory: {self.cache_dir}")
        print("This may take a while depending on your internet connection.")
        
        try:
            # Download the model snapshot
            snapshot_download(
                repo_id=model_name_or_path,
                cache_dir=self.cache_dir,
                resume_download=True,
                max_workers=4
            )
            print(f"Model '{model_name_or_path}' downloaded successfully!")
        except Exception as e:
            print(f"Error downloading model: {e}")
            raise
    
    def load_model(self):
        """Load the AgentCPM model and tokenizer."""
        model_name_or_path = self.config.get("path", self.config.get("name"))
        
        if not model_name_or_path:
            raise ValueError("Model name or path is required")
        
        # Download model if it doesn't exist locally
        self.download_model(model_name_or_path)
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path,
            trust_remote_code=True,
            cache_dir=self.cache_dir
        )
        
        # Load model with optional quantization
        quantization_config = self.config.get("quantization", {})
        if quantization_config.get("enabled", False):
            # Use bitsandbytes for quantization
            from transformers import BitsAndBytesConfig
            
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=quantization_config.get("bits") == 4,
                load_in_8bit=quantization_config.get("bits") == 8,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name_or_path,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
                cache_dir=self.cache_dir
            )
        else:
            # Load model without quantization
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name_or_path,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
                cache_dir=self.cache_dir
            )
        
        # Move model to device if device_map is not used
        if self.device != "auto":
            self.model.to(self.device)
        
        self.model.eval()
        
        return self
    
    def generate_text(self, prompt, **kwargs):
        """Generate text based on the given prompt."""
        if not self.model or not self.tokenizer:
            self.load_model()
        
        # Use default parameters if not provided
        generate_params = {
            "max_length": self.config.get("params", {}).get("max_length", 2048),
            "temperature": self.config.get("params", {}).get("temperature", 0.7),
            "top_p": self.config.get("params", {}).get("top_p", 0.95),
            "top_k": self.config.get("params", {}).get("top_k", 50),
            "repetition_penalty": self.config.get("params", {}).get("repetition_penalty", 1.0),
            "do_sample": self.config.get("params", {}).get("do_sample", True),
            **kwargs
        }
        
        # Encode prompt
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        
        # Generate text
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                **generate_params
            )
        
        # Decode and return the generated text
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Return only the generated part (not including the prompt)
        return generated_text[len(prompt):]
    
    def generate_text_stream(self, prompt, **kwargs):
        """Generate text in a streaming manner."""
        if not self.model or not self.tokenizer:
            self.load_model()
        
        # Use default parameters if not provided
        generate_params = {
            "max_length": self.config.get("params", {}).get("max_length", 2048),
            "temperature": self.config.get("params", {}).get("temperature", 0.7),
            "top_p": self.config.get("params", {}).get("top_p", 0.95),
            "top_k": self.config.get("params", {}).get("top_k", 50),
            "repetition_penalty": self.config.get("params", {}).get("repetition_penalty", 1.0),
            "do_sample": self.config.get("params", {}).get("do_sample", True),
            "streamer": self.tokenizer,
            **kwargs
        }
        
        # Encode prompt
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        
        # Generate text with streaming
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                **generate_params
            )
        
        # Decode and return the generated text
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Return only the generated part (not including the prompt)
        return generated_text[len(prompt):]
    
    def get_model_info(self):
        """Get model information."""
        if not self.model:
            self.load_model()
        
        return {
            "model_name": self.config.get("name"),
            "model_path": self.config.get("path"),
            "device": self.device,
            "model_size": f"{self.model.num_parameters():,} parameters",
            "quantization": self.config.get("quantization", {})
        }

# 全局实例将在CPMAgent初始化时创建
