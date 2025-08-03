import json
from openai import OpenAI
from models import Email
import inspect

from agent_tools.tools import schedule_meeting, draft_reply, add_to_todo_list

def get_tools_specs():
    """
    Generates a simplified list of tool specifications for the LLM.
    We use Python's 'inspect' module to automatically get function descriptions.
    """
    tools_for_llm = []
    tool_functions = [schedule_meeting, draft_reply, add_to_todo_list]
    for func in tool_functions:
        # Get the function's docstring and format it
        docstring = inspect.getdoc(func)
        # Construct the spec string
        spec = f"- {func.__name__}: {docstring.strip()}"
        tools_for_llm.append(spec)
    return "\n".join(tools_for_llm)

class Planner:
    def __init__(self):
        self.client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
        self.system_prompt = f"""
            You are an expert planning agent. Your task is to create a plan to handle an email.
            Based on the email's content and summary, decide which tools (if any) are needed.

            You have access to the following tools:
            {get_tools_specs()}

            Your output MUST be a valid JSON list of tool calls. Each item in the list is a dictionary
            representing one tool call, with two keys: 'tool_name' and 'arguments'.
            The 'arguments' must be a dictionary of key-value pairs.

            If no action is needed, return an empty list: [].

            Example plan for an email asking to schedule a call:
            [
                {{
                    "tool_name": "schedule_meeting",
                    "arguments": {{
                    "attendees": ["sender@example.com"],
                    "topic": "Project Discussion",
                    "duration_minutes": 30
                    }}
                }}
            ]
            """

    def generate_plan(self, email: Email) -> list[dict]:
        """Generates a plan of tool calls based on the email."""
        user_prompt = f"""
            Here is the email to process:
            - From: {email.sender}
            - Subject: {email.subject}
            - Summary: {email.summary}

            Create a plan as a JSON list of tool calls.
            """
        try:
            response = self.client.chat.completions.create(
                model="phi3:mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            response_text = response.choices[0].message.content
            plan_json = json.loads(response_text)
            return plan_json
        except Exception as e:
            print(f"Error generating plan: {e}")
            return [] 