from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.chatbot import Chatbot
from tools.calculator import calculator_tool, calculate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Define tools for the chatbot
tool_schemas = [calculator_tool]
tool_functions = {"calculate": calculate}

# Initialize the chatbot
chatbot = Chatbot(tool_schemas, tool_functions)

@app.route('/')
def index():
    """Render the chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle user messages and return chatbot responses."""
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
            
        response = chatbot.process_message(user_message)
        return jsonify({'response': response})
    except Exception as e:
        app.logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY environment variable not set. The chatbot will not function properly.")
    else:
        print(f"Using OpenAI API key (first 10 chars): {api_key[:10]}...")
    
    # Enable more verbose logging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Run the app with modified host parameter to allow external access
    # Using port 8080 instead of 5000 to avoid conflict with AirPlay Receiver on macOS
    print("Starting Flask server on http://127.0.0.1:8080 and http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)