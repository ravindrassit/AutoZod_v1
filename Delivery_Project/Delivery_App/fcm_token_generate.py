import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from django.conf import settings


# Path to the service account key file
# SERVICE_ACCOUNT_FILE = 'path/to/your-service-account-key.json'
SERVICE_ACCOUNT_FILE = "C:/Zaperr/BE/zaperr-288b8-500d42cab2eb.json"


def fcm_token():
    # Define the required scope
    SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

    # Authenticate with the service account key
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    credentials.refresh(Request())  # Refresh the token

    # Get the OAuth2.0 token
    token = credentials.token
    # print(f"Access Token: {token}")
    return token

if __name__ == "__main__":
    result = fcm_token()
    print(result)