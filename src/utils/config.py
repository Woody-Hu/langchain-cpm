import os
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConfigManager:
    """Configuration manager for loading and accessing YAML configuration files."""
    
    def __init__(self):
        self.configs = {}
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        
    def load_config(self, config_name):
        """Load a configuration file by name."""
        config_path = os.path.join(self.config_dir, f"{config_name}_config.yaml")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                self.configs[config_name] = yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    def load_all_configs(self):
        """Load all configuration files."""
        config_files = os.listdir(self.config_dir)
        for file in config_files:
            if file.endswith("_config.yaml"):
                config_name = file.replace("_config.yaml", "")
                self.load_config(config_name)
    
    def get(self, config_path, default=None):
        """Get a configuration value by path (e.g., 'model.params.max_length')."""
        parts = config_path.split(".")
        value = self.configs
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def get_env(self, env_var, default=None):
        """Get an environment variable value."""
        return os.getenv(env_var, default)
    
    def merge_with_env(self):
        """Merge configuration with environment variables."""
        # Merge model configuration with environment variables
        if "model" in self.configs:
            self.configs["model"]["name"] = self.get_env("MODEL_NAME", self.configs["model"].get("name"))
            self.configs["model"]["path"] = self.get_env("MODEL_PATH", self.configs["model"].get("path"))
            if "params" in self.configs["model"]:
                self.configs["model"]["params"]["max_length"] = int(self.get_env("MODEL_MAX_LENGTH", self.configs["model"]["params"].get("max_length")))
                self.configs["model"]["params"]["temperature"] = float(self.get_env("MODEL_TEMPERATURE", self.configs["model"]["params"].get("temperature")))
        
        # Merge agent configuration with environment variables
        if "agent" in self.configs:
            self.configs["agent"]["max_steps"] = int(self.get_env("AGENT_MAX_STEPS", self.configs["agent"].get("max_steps")))
            self.configs["agent"]["timeout"] = int(self.get_env("AGENT_TIMEOUT", self.configs["agent"].get("timeout")))

# Create a global instance of ConfigManager
config_manager = ConfigManager()
