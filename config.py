from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv


# Load the environment variables
load_dotenv()

# Initialize Fernet with the key
f = Fernet(key)

# Encrypt the API keys
google_key = os.getenv('GOOGLE_API_KEY').encode()
tavily_key = os.getenv('TAVILY_API_KEY').encode()

encrypted_google = f.encrypt(google_key)
encrypted_tavily = f.encrypt(tavily_key)

# Create new .env with encrypted keys
with open('.env', 'w') as env_file:
    env_file.write(f'ENCRYPTED_GOOGLE_KEY="{encrypted_google.decode()}"\n')
    env_file.write(f'ENCRYPTED_TAVILY_KEY="{encrypted_tavily.decode()}"')