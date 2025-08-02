import os.path
import base64
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models import Email

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "gmail_api_credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def fetch_latest_emails(max_results=5) -> list[Email]:
    creds = get_credentials()
    emails_data = []
    try:
        service = build("gmail", "v1", credentials=creds)
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
            subject, sender, received_date_str = "No Subject", "No Sender", ""
            
            for header in headers:
                if header["name"] == "Subject": subject = header["value"]
                if header["name"] == "From": sender = header["value"]
                if header["name"] == "Date": received_date_str = header["value"]

            try:
                received_date = datetime.strptime(received_date_str.split(' (')[0].strip(), '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                received_date = datetime.now()

            body = ""
            if "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain":
                        if body_data := part.get("body", {}).get("data"):
                            body = base64.urlsafe_b64decode(body_data).decode("utf-8")
                            break
            elif body_data := payload.get("body", {}).get("data"):
                body = base64.urlsafe_b64decode(body_data).decode("utf-8")

            emails_data.append(Email(
                id=msg["id"], sender=sender, subject=subject,
                body=body.strip(), received_at=received_date
            ))
        
        return emails_data
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []