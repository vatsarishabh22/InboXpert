import json
import requests
from models import Email
from openai import OpenAI
        
class Planner:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url
        self.client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
        self.system_prompt = f"""
            You are an expert planning agent. Your task is to create a plan to handle an email.
            Based on the email's content and summary, decide which tools (if any) are needed.

            You have access to the following tools:
            {self._get_tools_from_server()}

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

    def _get_tools_from_server(self) -> str:
        """Fetches tool specifications dynamically from the MCP server."""
        try:
            response = requests.get(f"{self.server_url}/listTools")
            response.raise_for_status()
            tools = response.json().get("tools", [])
            
            specs = [f"- {t['tool_name']}: {t['description']}" for t in tools]
            return "\n".join(specs)
        except requests.RequestException as e:
            print(f"ERROR: Could not fetch tools from server: {e}")
            return "No tools available."

    
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

