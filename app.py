from email_client import fetch_latest_emails
from strategies import LLMCategorizerStrategy

def main():
    """
    Main function to run the email fetching and categorization process.
    """

    print("Starting email handler...")
    
    # TODO: Add  categorizer = EmbeddingCategorizerStrategy()
    categorizer = LLMCategorizerStrategy()
    latest_emails = fetch_latest_emails(max_results=5)
    
    if not latest_emails:
        print("No emails to process. Exiting.")
        return

    print("\n--- Analyzing your latest emails ---\n")
    for i, email in enumerate(latest_emails):
        print(f"--- Processing Email #{i+1}: '{email.subject}' ---")

        category, summary = categorizer.categorize(email)
        email.category = category
        email.summary = summary
        
        print(f"Category: {email.category}")
        print(f"Summary: {email.summary}")
        print("-" * (25 + len(email.subject)))
        print()


if __name__ == "__main__":
    main()