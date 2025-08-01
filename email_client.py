import os.path
import base64
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models import Email

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_credentials():
    """Gets user credentials for the Gmail API."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "gmail_api_credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def fetch_latest_emails(max_results=5) -> list[Email]:
    """Fetches the latest unread emails and parses them into Email objects."""
    creds = get_credentials()
    emails_data = []

    try:
        service = build("gmail", "v1", credentials=creds)
        # Get a list of message IDs for unread emails
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX", "UNREAD"], maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])

        if not messages:
            print("No new unread messages found.")
            return []

        print(f"Found {len(messages)} unread messages. Fetching details...")
        for message_info in messages:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=message_info["id"], format="full")
                .execute()
            )
            
            payload = msg.get("payload", {})
            headers = payload.get("headers", [])
            
            subject = "No Subject"
            sender = "No Sender"
            received_date_str = ""
            
            for header in headers:
                if header["name"] == "Subject":
                    subject = header["value"]
                if header["name"] == "From":
                    sender = header["value"]
                if header["name"] == "Date":
                    received_date_str = header["value"]

            # Parse date, handling potential timezone info
            try:
                # Example format: "Thu, 25 Jul 2024 12:34:56 +0530"
                # The format can vary, this is a common one.
                received_date = datetime.strptime(received_date_str.split(' (')[0].strip(), '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                received_date = datetime.now()


            # Get the email body
            body = ""
            if "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain":
                        body_data = part["body"].get("data")
                        if body_data:
                            body = base64.urlsafe_b64decode(body_data).decode("utf-8")
                            break # Stop after finding the first plain text part
            else: # If not multipart
                 body_data = payload.get("body", {}).get("data")
                 if body_data:
                    body = base64.urlsafe_b64decode(body_data).decode("utf-8")


            emails_data.append(Email(
                id=msg["id"],
                sender=sender,
                subject=subject,
                body=body.strip(),
                received_at=received_date,
            ))
        
        return emails_data

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []