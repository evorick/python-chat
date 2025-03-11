import os
import sys
import logging
from openai import OpenAI
import json
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY environment variable not set. Please set it in your .env file.")
    sys.exit(1)
else:
    logger.info(f"Using OpenAI API key (first 10 chars): {api_key[:10]}...")

# Initialize the OpenAI client
try:
    client = OpenAI(api_key=api_key)
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {str(e)}")
    sys.exit(1)

class Chatbot:
    def __init__(self, tool_schemas, tool_functions):
        """Initialize the chatbot with tool schemas and functions."""
        self.messages = []  # Store conversation history
        self.tool_schemas = tool_schemas  # List of tool schemas for OpenAI API
        self.tool_functions = tool_functions  # Dictionary of tool functions
        logger.info("Chatbot initialized with %d tools", len(tool_schemas))

    def process_message(self, user_message):
        """Process a user message and return the chatbot's response."""
        try:
            # Add user message to conversation history
            self.messages.append({"role": "user", "content": user_message})
            logger.info("Processing user message: %s", user_message[:50] + "..." if len(user_message) > 50 else user_message)

            # Call OpenAI API with current messages and tools
            try:
                logger.info("Calling OpenAI API...")
                response = client.chat.completions.create(
                    model="gpt-4",  # Use an appropriate model
                    messages=self.messages,
                    tools=self.tool_schemas,
                )
                logger.info("OpenAI API response received")
                assistant_message = response.choices[0].message
                self.messages.append(assistant_message)
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {str(e)}")
                # Try again with a different model if the first one fails
                try:
                    logger.info("Retrying with gpt-3.5-turbo model...")
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=self.messages,
                        tools=self.tool_schemas,
                    )
                    logger.info("OpenAI API retry successful")
                    assistant_message = response.choices[0].message
                    self.messages.append(assistant_message)
                except Exception as retry_error:
                    logger.error(f"Error on retry: {str(retry_error)}")
                    return f"Error connecting to OpenAI: {str(e)}. Please check your API key and try again."

            # Handle tool calls if present
            if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                logger.info("Processing %d tool calls", len(assistant_message.tool_calls))
                while assistant_message.tool_calls:
                    for tool_call in assistant_message.tool_calls:
                        try:
                            tool_name = tool_call.function.name
                            logger.info(f"Executing tool: {tool_name}")
                            arguments = json.loads(tool_call.function.arguments)
                            # Execute the tool function
                            result = self.tool_functions[tool_name](**arguments)
                            logger.info(f"Tool execution successful: {tool_name}")
                            # Add tool result to conversation history
                            self.messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": result,
                            })
                        except Exception as e:
                            # Handle errors in tool execution
                            error_message = f"Error executing tool {tool_name}: {str(e)}"
                            logger.error(error_message)
                            self.messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": error_message,
                            })
                    
                    # Call the API again with updated messages
                    try:
                        logger.info("Calling OpenAI API again after tool execution...")
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=self.messages,
                            tools=self.tool_schemas,
                        )
                        logger.info("OpenAI API response received after tool execution")
                        assistant_message = response.choices[0].message
                        self.messages.append(assistant_message)
                    except Exception as e:
                        logger.error(f"Error getting response from OpenAI after tool execution: {str(e)}")
                        return f"Error getting response from OpenAI: {str(e)}"

            logger.info("Returning assistant response")
            return assistant_message.content
        except Exception as e:
            logger.error(f"Unexpected error in process_message: {str(e)}")
            return f"An unexpected error occurred: {str(e)}"