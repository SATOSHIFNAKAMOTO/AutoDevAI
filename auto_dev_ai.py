import autogen
import time
import os
from threading import Thread

# Configure the AI agents
config_list = [
    {
        "model": "codellama/CodeLlama-34b-Instruct-hf",  # Using CodeLlama as an example of a locally-run model
        "api_base": "http://localhost:8000",  # Assuming the model is served locally
        "api_type": "open_ai",
        "api_key": "NOT_NEEDED"  # Local models typically don't need an API key
    }
]

# Create a CEO agent (you)
ceo = autogen.UserProxyAgent(
    name="CEO",
    system_message="You are the CEO of the AI software company. You provide high-level direction and business insights.",
    human_input_mode="TERMINATE",
    code_execution_config={"work_dir": "company_projects", "use_docker": False},
)

# Create a product manager agent
product_manager = autogen.AssistantAgent(
    name="ProductManager",
    system_message="You are a product manager who translates business requirements into product features and roadmaps.",
    llm_config={"config_list": config_list},
)

# Create a software architect agent
architect = autogen.AssistantAgent(
    name="SoftwareArchitect",
    system_message="You are a software architect who designs high-level software structures and makes technology choices.",
    llm_config={"config_list": config_list},
)

# Create a lead developer agent
lead_developer = autogen.AssistantAgent(
    name="LeadDeveloper",
    system_message="You are a lead developer who implements solutions, writes code, and manages the development process.",
    llm_config={"config_list": config_list},
)

# Create a QA engineer agent
qa_engineer = autogen.AssistantAgent(
    name="QAEngineer",
    system_message="You are a QA engineer responsible for testing, identifying bugs, and ensuring software quality.",
    llm_config={"config_list": config_list},
)

def continuous_development_cycle():
    while True:
        # Start a new project or continue existing ones
        ceo.initiate_chat(
            product_manager,
            message="What's the next feature or improvement we should work on for our software?"
        )
        
        # Product Manager discusses with Architect
        product_manager.initiate_chat(
            architect,
            message="Based on the CEO's input, how should we design this feature?"
        )
        
        # Architect discusses with Lead Developer
        architect.initiate_chat(
            lead_developer,
            message="Here's the design. Please implement this feature."
        )
        
        # Lead Developer codes and then discusses with QA Engineer
        lead_developer.initiate_chat(
            qa_engineer,
            message="I've implemented the feature. Please test it thoroughly."
        )
        
        # QA Engineer reports back to CEO
        qa_engineer.initiate_chat(
            ceo,
            message="Here are the results of our latest development cycle."
        )
        
        # Short pause before starting the next cycle
        time.sleep(60)  # Adjust as needed

# Start the continuous development cycle in a separate thread
dev_thread = Thread(target=continuous_development_cycle)
dev_thread.start()

# Main program loop
print("AI Software Company is now running. Press Ctrl+C to stop.")
try:
    while True:
        # Check for any manual input or commands
        if os.path.exists("ceo_input.txt"):
            with open("ceo_input.txt", "r") as f:
                ceo_message = f.read().strip()
            os.remove("ceo_input.txt")
            ceo.initiate_chat(
                product_manager,
                message=f"New direction from CEO: {ceo_message}"
            )
        time.sleep(10)  # Check for input every 10 seconds
except KeyboardInterrupt:
    print("Shutting down AI Software Company...")