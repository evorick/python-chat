import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key (first 10 chars): {api_key[:10]}...")

# Initialize client
client = OpenAI(api_key=api_key)

try:
    # Test API connection
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello, world!"}]
    )
    print("API Connection Successful!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error: {e}")
