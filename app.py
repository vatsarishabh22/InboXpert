from email_client import fetch_latest_emails

def main():
    """
    Main function to run the email fetching process.
    """
    print("Starting email handler...")
    latest_emails = fetch_latest_emails(max_results=5)
    
    if not latest_emails:
        print("No emails to process. Exiting.")
        return

    print("\n--- Here are your latest emails ---\n")
    for i, email in enumerate(latest_emails):
        print(f"--- Email #{i+1} ---")
        print(f"  Subject: {email.subject}")
        print(f"     From: {email.sender}")
        print(f" Received: {email.received_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Body: {email.body[:100]}...") 
        print("-" * (len(str(i+1))+11)) # Prints a line like "--- Email #1 ---"
        print()


if __name__ == "__main__":
    main()