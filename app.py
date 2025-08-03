from email_client import fetch_latest_emails
from strategies import LLMCategorizerStrategy
from agents.planner import Planner
from agents.executor import execute_plan

def main():
    """
    Main function to run the email fetching and categorization process.
    """
    print("Starting email handler...")
    
    # --- Setup Phase ---
    # TODO: Add  categorizer = EmbeddingCategorizerStrategy()
    categorizer = LLMCategorizerStrategy()
    latest_emails = fetch_latest_emails(max_results=5)
    planner = Planner()
    
    # --- Run Phase ---
    if not latest_emails:
        print("No emails to process. Exiting.")
        return

    print("\n--- Processing Emails ---\n")
    for email in latest_emails:
        print(f"--- 1. Analyzing Email: '{email.subject}' ---")
        category, summary = categorizer.categorize(email)
        email.category = category
        email.summary = summary
        print(f"  -> Category: {email.category}")
        print(f"  -> Summary: {email.summary}")

        print(f"\n--- 2. Generating Plan for '{email.subject}' ---")
        plan = planner.generate_plan(email)
        print(f"  -> Generated Plan: {plan}")
        
        print(f"\n--- 3. Executing Plan for '{email.subject}' ---")
        execute_plan(plan)
        
        print("\n" + "="*50 + "\n") # Separator for the next email


if __name__ == "__main__":
    main()