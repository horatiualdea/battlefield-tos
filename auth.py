from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES
    )
    creds = flow.run_local_server(port=0)

    # Save the credentials
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())

    print("Authentication successful! Token saved.")

if __name__ == "__main__":
    authenticate_youtube()
