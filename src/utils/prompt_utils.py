import os
import yaml

class PromptManager:
    """Prompt manager for loading and rendering prompt templates."""
    
    def __init__(self):
        self.prompts = {}
        self.prompt_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")
        
    def load_prompt(self, prompt_name):
        """Load a prompt template by name."""
        prompt_path = os.path.join(self.prompt_dir, f"{prompt_name}.yaml")
        
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_data = yaml.safe_load(f)
                
            self.prompts.update(prompt_data)
            return prompt_data
        else:
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    def load_all_prompts(self):
        """Load all prompt templates."""
        # No prompt files to load currently
        pass

    def get_prompt(self, prompt_name):
        """Get a prompt template by name."""
        if prompt_name in self.prompts:
            return self.prompts[prompt_name]
        else:
            # Try to load the prompt if it's not already loaded
            self.load_prompt(prompt_name)
            return self.prompts.get(prompt_name)

    def render_prompt(self, prompt_name, **kwargs):
        """Render a prompt template with the given parameters."""
        prompt_template = self.get_prompt(prompt_name)
        if not prompt_template:
            raise KeyError(f"Prompt '{prompt_name}' not found")
        
        return prompt_template.format(**kwargs)

# Create a global instance of PromptManager
prompt_manager = PromptManager()
