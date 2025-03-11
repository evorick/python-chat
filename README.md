# OpenAI Chatbot Tutorial

This repository provides a template for building an OpenAI chatbot with a modern UI and OpenAI tool calling capabilities. The chatbot can perform calculations and can be extended with additional tools.

## Features

- Modern, responsive UI with a clean design
- OpenAI GPT-4 integration
- Tool calling capabilities (calculator example included)
- Error handling and input validation
- Environment variable management

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd chat
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Running the Application

1. **Start the Flask server:**
   ```bash
   python ui/app.py
   ```

2. **Access the chatbot:**
   - Open your browser and navigate to: `http://127.0.0.1:8080/`
   - Start chatting with the bot!

## Example Interactions

- Try asking the bot to calculate something: "Calculate 2 + 2"
- Ask general questions: "What is the capital of France?"
- Try more complex calculations: "Calculate the square root of 144"

## Extending the Chatbot

### Adding New Tools

1. Create a new file in the `tools` directory (e.g., `weather.py`)
2. Define your tool function and schema (see `calculator.py` for an example)
3. Import and register your tool in `app.py`

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly set in the `.env` file
- **Module Not Found Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Permission Denied**: If you encounter permission issues when running the application, check file permissions

## License

This project is licensed under the MIT License - see the LICENSE file for details.