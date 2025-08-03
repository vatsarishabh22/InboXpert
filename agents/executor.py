from agent_tools.tools import AVAILABLE_TOOLS

def execute_plan(plan: list[dict]):
    """
    Executes a plan by calling the appropriate tools.
    """
    if not plan:
        print("Plan is empty. No actions to execute.")
        return

    for action in plan:
        tool_name = action.get("tool_name")
        arguments = action.get("arguments")
        
        if tool_name not in AVAILABLE_TOOLS:
            print(f"Error: Tool '{tool_name}' not found.")
            continue
            
        tool_function = AVAILABLE_TOOLS[tool_name]
        
        print(f"\nExecuting tool: {tool_name}")
        try:
            result = tool_function(**arguments)
            print(f"  -> Result: {result}")
        except TypeError as e:
            print(f"  -> Error executing tool: Invalid arguments provided. {e}")