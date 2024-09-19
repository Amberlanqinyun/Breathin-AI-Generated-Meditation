from google_auth_oauthlib.flow import InstalledAppFlow

def get_refresh_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        '/Users/amberlan/Downloads/meditator-main/venv/client_secret.json',  # Ensure this path is correct
        scopes=['https://www.googleapis.com/auth/gmail.send']
    )
    flow.run_local_server(port=0)
    credentials = flow.credentials

    print("Access Token:", credentials.token)
    print("Refresh Token:", credentials.refresh_token)
    print("Token Expiry:", credentials.expiry)

if __name__ == "__main__":
    get_refresh_token()
