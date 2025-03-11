#!/usr/bin/env python3
"""
Simple script to directly test OpenAI API connectivity.
This will help diagnose if the issue is with the API key or with the Flask application.
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables")
    exit(1)

print(f"Using API key (first 10 chars): {api_key[:10]}...")

# Test direct API connection using requests
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello, world!"}]
}

print("Sending direct API request to OpenAI...")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        print(f"Success! Response: {content}")
    else:
        print(f"Error response: {response.text}")
        
        # Check for common error types
        if response.status_code == 401:
            print("\nAuthentication error: Your API key may be invalid or expired.")
        elif response.status_code == 403:
            print("\nAuthorization error: Your API key doesn't have permission to use this resource.")
            print("If you're using a Project API key, make sure it has access to the model you're trying to use.")
        elif response.status_code == 429:
            print("\nRate limit exceeded: You've hit OpenAI's rate limits.")
        
except Exception as e:
    print(f"Exception occurred: {str(e)}")

print("\nTest complete. If you see errors above, fix your API key before continuing.")
