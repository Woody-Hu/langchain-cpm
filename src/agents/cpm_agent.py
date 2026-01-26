from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.models.cpm_model import cpm_model
from src.utils.config import config_manager
from src.utils.prompt_utils import prompt_manager

# Define the state schema for the agent
class AgentState:
    """Agent state schema for the state graph."""
    
    def __init__(self):
        self.task = ""
        self.plan = []
        self.current_step = 0
        self.results = []
        self.progress = ""
        self.final_answer = ""

# Define the agent class
class CPMAgent:
    """AgentCPM agent based on LangChain DeepAgents."""
    
    def __init__(self):
        self.config = config_manager.get("agent", {})
        self.model = cpm_model
        self.memory = MemorySaver()
        self.graph = self._build_graph()
        
    def _build_graph(self):
        """Build the state graph for the agent."""
        # Define the nodes
        def plan_node(state):
            """Generate a plan for the task."""
            prompt = prompt_manager.render_prompt("planning", task=state.task)
            plan_text = self.model.generate_text(prompt)
            
            # Parse the plan into a list of steps
            plan = []
            for line in plan_text.split("\n"):
                if line.strip() and ":" in line:
                    step_number, step_description = line.split(":", 1)
                    plan.append(step_description.strip())
            
            return {
                "plan": plan,
                "current_step": 0,
                "results": [],
                "progress": "Planning completed"
            }
        
        def execute_node(state):
            """Execute the current step of the plan."""
            if state.current_step >= len(state.plan):
                return {
                    "progress": "Execution completed",
                    "final_answer": self._generate_final_answer(state)
                }
            
            current_step_desc = state.plan[state.current_step]
            prompt = prompt_manager.render_prompt(
                "execution",
                plan=state.plan,
                current_step=current_step_desc,
                previous_results=state.results
            )
            
            # For now, we'll just generate text as the result
            # In a real implementation, this would call tools
            result = self.model.generate_text(prompt)
            
            return {
                "current_step": state.current_step + 1,
                "results": state.results + [result],
                "progress": f"Executed step {state.current_step + 1}/{len(state.plan)}"
            }
        
        def reflect_node(state):
            """Reflect on the progress and adjust the plan if necessary."""
            if not self.config.get("reflection", {}).get("enabled", True):
                return state
            
            prompt = prompt_manager.render_prompt(
                "reflection",
                task=state.task,
                plan=state.plan,
                progress=state.progress,
                results=state.results
            )
            
            reflection = self.model.generate_text(prompt)
            
            # For now, we'll just add the reflection to the results
            # In a real implementation, this would adjust the plan
            return {
                "results": state.results + [f"Reflection: {reflection}"],
                "progress": f"Reflection completed: {state.progress}"
            }
        
        def should_continue(state):
            """Decide whether to continue execution or finish."""
            if state.current_step >= len(state.plan):
                return "finish"
            elif self.config.get("reflection", {}).get("enabled", True) and \
                 state.current_step % self.config.get("reflection", {}).get("frequency", 5) == 0:
                return "reflect"
            else:
                return "execute"
        
        # Create the state graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("plan", plan_node)
        workflow.add_node("execute", execute_node)
        workflow.add_node("reflect", reflect_node)
        workflow.add_node("finish", self._finish_node)
        
        # Add edges
        workflow.set_entry_point("plan")
        workflow.add_edge("plan", "execute")
        workflow.add_conditional_edges(
            "execute",
            should_continue,
            {
                "execute": "execute",
                "reflect": "reflect",
                "finish": "finish"
            }
        )
        workflow.add_edge("reflect", "execute")
        workflow.add_edge("finish", END)
        
        # Compile the graph with memory
        return workflow.compile(checkpointer=self.memory)
    
    def _finish_node(self, state):
        """Generate the final answer and finish the task."""
        final_answer = self._generate_final_answer(state)
        return {
            "final_answer": final_answer,
            "progress": "Task completed"
        }
    
    def _generate_final_answer(self, state):
        """Generate the final answer based on the results."""
        prompt = prompt_manager.render_prompt(
            "final_summary",
            task=state.task,
            plan=state.plan,
            results=state.results
        )
        
        return self.model.generate_text(prompt)
    
    def run(self, task, config=None):
        """Run the agent on a given task."""
        # Update config if provided
        if config:
            self.config.update(config)
        
        # Initialize state
        initial_state = {
            "task": task,
            "plan": [],
            "current_step": 0,
            "results": [],
            "progress": "Initializing"
        }
        
        # Run the graph
        final_state = None
        for state in self.graph.stream(initial_state, {"configurable": {"thread_id": "test-thread"}}):
            final_state = state
            
        return final_state.get("final_answer", "No final answer generated")

# Create a global instance of CPMAgent
cpm_agent = CPMAgent()
