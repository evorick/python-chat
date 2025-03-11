import math

def calculate(expression):
    """Evaluate a mathematical expression."""
    try:
        # Safely evaluate the expression with restricted globals
        return str(eval(expression, {"__builtins__": None}, {"math": math}))
    except Exception as e:
        return str(e)

calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a mathematical expression",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g., '2 + 2'",
                },
            },
            "required": ["expression"],
        },
    },
}