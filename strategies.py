import json
from abc import ABC, abstractmethod
from openai import OpenAI
from models import Email


class CategorizationStrategy(ABC):
    """
    An abstract base class for all categorization strategies.
    It declares a 'categorize' method that all concrete strategies must implement.
    """
    @abstractmethod
    def categorize(self, email: Email) -> tuple[str, str]:
        """Takes an Email object and returns its category and a summary."""
        pass


class LLMCategorizerStrategy(CategorizationStrategy):
    """
    The concrete implementation of the strategy that uses a local LLM.
    """
    def __init__(self):
        self.client = OpenAI(
            base_url='http://localhost:11434/v1',
            api_key='ollama',
        )
        self.system_prompt = """
            You are an expert email analysis assistant. Your task is to analyze an email and return a structured JSON object.
            The JSON object must have two keys:
            1. "category": Classify the email into one of the following categories: ["Invoice", "Meeting Request", "Job Application", "Spam/Marketing", "Personal Conversation", "Urgent Inquiry"].
            2. "summary": Provide a one-sentence summary of the email's content.
            Analyze the email content provided and respond only with the valid JSON object.
        """

    def categorize(self, email: Email) -> tuple[str, str]:
        """Categorizes an email using the local LLM via Ollama."""
        try:
            response = self.client.chat.completions.create(
                model="phi3:mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Please analyze this email:\n\n{email.body}"}
                ]
            )
            
            response_text = response.choices[0].message.content
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in the response.")
                
            json_string = response_text[json_start:json_end]
            result = json.loads(json_string)
            
            category = result.get("category", "Uncategorized")
            summary = result.get("summary", "Could not summarize.")
            
            return category, summary

        except Exception as e:
            print(f"An error occurred while calling the local LLM: {e}")
            return "Error", "Failed to process email locally."
        

class EmbeddingCategorizerStrategy(CategorizationStrategy):
    """
    The concrete implementation of the strategy that uses a Embeddings LLM.
    """
    def categorize(self, email: Email) -> tuple[str, str]:
        # 1. Use Qwen2 to get embedding of email.body
        # 2. Compare this embedding to pre-computed embeddings for each category
        # 3. Find the closest match
        print("Using Embedding Strategy...")
        # ... logic for embedding comparison ...
        return 
