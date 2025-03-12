# Import Flask-related modules for building a web application
from flask import Flask, render_template, request, jsonify
# - Flask: The main class to create a web server
# - render_template: Function to render HTML templates
# - request: Object to handle incoming HTTP requests (e.g., POST data)
# - jsonify: Function to convert Python dictionaries to JSON responses

# Import sys for system-level operations, like modifying the Python path
import sys
# - sys provides access to Python interpreter variables and functions

# Import os for operating system interactions, like file path manipulation
import os
# - os provides a portable way to interact with the operating system

# Modify the Python module search path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# - sys.path: A list of directories Python searches for modules
# - sys.path.insert(0, ...): Adds a directory to the start of the search path (0 means highest priority)
# - os.path.dirname(__file__): Gets the directory of the current script (e.g., "/path/to/script")
# - os.path.join(..., '..'): Joins the script's directory with ".." to go up one level (parent directory)
# - os.path.abspath(...): Converts the relative path to an absolute path (e.g., "/path/to/parent")
# - Purpose: Allows importing modules (like agent.chatbot) from the parent directory

# Import the Chatbot class from a custom module in the parent directory
from agent.chatbot import Chatbot
# - agent.chatbot: Assumes a module "chatbot.py" exists in an "agent" folder in the parent directory
# - Chatbot: A class (presumably) that handles chat logic, likely using an AI model

# Import calculator-related tools from a custom module
from tools.calculator import calculator_tool, calculate
# - tools.calculator: Assumes a module "calculator.py" exists in a "tools" folder
# - calculator_tool: Likely a schema or definition of the calculator tool (e.g., for tool-calling APIs)
# - calculate: A function that performs calculations, to be used by the chatbot

# Import load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv
# - dotenv: A third-party package (requires `pip install python-dotenv`)
# - load_dotenv: Reads key-value pairs from a .env file and sets them as environment variables

# Load environment variables from the .env file in the current directory
load_dotenv()
# - Looks for a .env file (e.g., "OPENAI_API_KEY=your-key") in the same directory as this script
# - Loads variables into os.environ, making them accessible via os.getenv()
# - No arguments means it uses the default path (current working directory)

# Create a Flask application instance
app = Flask(__name__)
# - Flask(__name__): Initializes a Flask app
# - __name__: A Python built-in variable; here, it’s "__main__" if run directly, or the module name if imported
# - Purpose: Sets up the web server with this script as the main module

# Define a list of tool schemas for the chatbot
tool_schemas = [calculator_tool]
# - tool_schemas: A list containing tool definitions (here, just calculator_tool)
# - calculator_tool: Likely a dictionary or object defining the calculator tool’s structure
# - Purpose: Passed to the Chatbot to specify available tools it can use

# Define a dictionary mapping tool names to their corresponding functions
tool_functions = {"calculate": calculate}
# - tool_functions: A dictionary where keys are tool names and values are callable functions
# - "calculate": The key matches a tool name (likely referenced in calculator_tool)
# - calculate: The actual function from tools.calculator that performs the calculation
# - Purpose: Links tool names to their implementations for the Chatbot to execute

# Initialize an instance of the Chatbot class with tools
chatbot = Chatbot(tool_schemas, tool_functions)
# - Chatbot(...): Creates a new Chatbot object
# - tool_schemas: Passes the list of tool definitions
# - tool_functions: Passes the dictionary of tool implementations
# - Assumption: Chatbot class uses these to process messages and call tools as needed

# Define a route for the root URL ("/") using a decorator
@app.route('/')
def index():
    """Render the chat interface."""
    # - @app.route('/'): Associates the "/" URL with the index() function
    # - Docstring: A short description of the function’s purpose
    return render_template('index.html')
    # - render_template('index.html'): Renders an HTML file named "index.html"
    # - Assumes "index.html" exists in a "templates" folder (Flask’s default template directory)
    # - Returns: The rendered HTML as the HTTP response, displaying the chat interface

# Define a route for "/chat" that accepts POST requests
@app.route('/chat', methods=['POST'])
def chat():
    """Handle user messages and return chatbot responses."""
    # - @app.route('/chat', methods=['POST']): Associates "/chat" with chat(), only for POST requests
    # - methods=['POST']: Restricts this endpoint to HTTP POST requests (e.g., from a form or AJAX)
    # - Docstring: Describes the function’s role in processing chat messages
    
    try:
        # Start a block to catch and handle potential errors
        data = request.json
        # - request: Flask’s request object, containing incoming HTTP request data
        # - request.json: Parses the request body as JSON (expects Content-Type: application/json)
        # - data: A Python dictionary from the JSON (e.g., {"message": "Hi"})
        # - Assumption: The client sends JSON with a "message" key

        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
            # - if not data: Checks if data is None or empty
            # - 'message' not in data: Checks if the "message" key is missing
            # - jsonify(...): Converts a Python dict to a JSON response
            # - {'error': 'No message provided'}: The response body indicating the error
            # - 400: HTTP status code for "Bad Request"
            # - Returns: Ends the function early with an error response

        user_message = data['message'].strip()
        # - data['message']: Extracts the value of the "message" key (e.g., "Hi ")
        # - .strip(): Removes leading/trailing whitespace (e.g., "Hi ")
        # - user_message: Stores the cleaned-up user input

        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
            # - if not user_message: Checks if the message is empty after stripping (e.g., "" or " ")
            # - jsonify(...): Returns a JSON error response
            # - 400: Indicates a bad request due to no meaningful input
            # - Returns: Ends the function early with an error

        response = chatbot.process_message(user_message)
        # - chatbot.process_message(...): Calls the Chatbot’s method to handle the message
        # - user_message: The cleaned input passed to the chatbot
        # - response: The chatbot’s output (assumed to be a string or dict)
        # - Assumption: process_message() uses the tools if needed and returns a response

        return jsonify({'response': response})
        # - jsonify(...): Converts the response to JSON
        # - {'response': response}: The response body with the chatbot’s reply
        # - Returns: Sends the successful response to the client (HTTP 200 by default)

    except Exception as e:
        # Catch any errors that occur in the try block
        app.logger.error(f"Error processing chat request: {str(e)}")
        # - app.logger: Flask’s built-in logging object
        # - .error(...): Logs the error at the ERROR level
        # - f"Error processing chat request: {str(e)}": Formats the error message with details
        # - Purpose: Logs the issue for debugging (visible if logging is configured)

        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
        # - jsonify(...): Returns a JSON error response
        # - {'error': ...}: Includes the error message for the client
        # - 500: HTTP status code for "Internal Server Error"
        # - Returns: Ends the function with an error response

# Check if this script is being run directly (not imported as a module)
if __name__ == '__main__':
    # - __name__: "__main__" if run directly, otherwise the module name
    # - Purpose: Ensures the following code only runs when this file is executed

    # Check if the OpenAI API key is set in the environment
    api_key = os.getenv("OPENAI_API_KEY")
    # - os.getenv(...): Retrieves the value of "OPENAI_API_KEY" from environment variables
    # - Returns None if the variable isn’t set (e.g., .env missing or key not defined)
    # - api_key: Stores the API key or None

    if not api_key:
        print("Warning: OPENAI_API_KEY environment variable not set. The chatbot will not function properly.")
        # - if not api_key: Checks if api_key is None or empty
        # - print(...): Outputs a warning to the console
        # - Purpose: Alerts the user to a critical configuration issue
    else:
        print(f"Using OpenAI API key (first 10 chars): {api_key[:10]}...")
        # - else: Runs if api_key exists
        # - api_key[:10]: Shows the first 10 characters of the key (for security)
        # - f-string: Formats the output (e.g., "Using OpenAI API key: sk-abc1234...")
        # - Purpose: Confirms the key is loaded without exposing it fully

    # Enable verbose logging for debugging
    import logging
    # - logging: Python’s built-in logging module
    # - Imported here to keep imports minimal unless needed
    logging.basicConfig(level=logging.DEBUG)
    # - logging.basicConfig(...): Configures the root logger
    # - level=logging.DEBUG: Sets the logging level to DEBUG (most verbose)
    # - Effect: Logs DEBUG, INFO, WARNING, ERROR, and CRITICAL messages
    # - Visible in the console due to default handler

    # Start the Flask development server
    print("Starting Flask server on http://127.0.0.1:8080 and http://localhost:8080")
    # - print(...): Informs the user where the server is running
    # - 127.0.0.1 and localhost: Common loopback addresses for local access
    # - 8080: The port number chosen below
    app.run(debug=True, host='0.0.0.0', port=8080)
    # - app.run(...): Starts the Flask web server
    # - debug=True: Enables debug mode (auto-reloads on code changes, shows detailed errors)
    # - host='0.0.0.0': Makes the server accessible externally (not just localhost)
    # - port=8080: Runs on port 8080 (avoids 5000, which macOS AirPlay might use)
    # - Effect: Server listens on all network interfaces at port 8080