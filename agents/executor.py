import requests

def execute_plan(plan: list[dict], server_url="http://localhost:8000"):
    """
    Shows a plan to the user, asks for confirmation, and then executes it.
    """
    if not plan:
        print("Plan is empty. No actions to execute.")
        return

    print("\n--- Proposed Plan ---")
    for i, action in enumerate(plan):
        print(f"{i+1}. Tool: {action['tool_name']}")
        print(f"   Arguments: {action['arguments']}")
    print("--------------------")

    confirm = input("Do you want to execute this plan? (y/n): ")
    if confirm.lower() != 'y':
        print("Execution cancelled.")
        return

    print("\nExecuting plan via MCP Server...")
    for action in plan:
        print(f"  -> Calling tool '{action['tool_name']}' on server...")
        try:
            response = requests.post(f"{server_url}/executeTool", json=action)
            response.raise_for_status()
            result = response.json()
            print(f"     Result: {result}")
        except requests.RequestException as e:
            print(f"     ERROR: Failed to execute tool '{action['tool_name']}': {e}")