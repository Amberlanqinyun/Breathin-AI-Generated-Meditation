import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print the Google OAuth credentials
print("GOOGLE_CLIENT_ID:", os.getenv('GOOGLE_CLIENT_ID'))
print("GOOGLE_CLIENT_SECRET:", os.getenv('GOOGLE_CLIENT_SECRET'))