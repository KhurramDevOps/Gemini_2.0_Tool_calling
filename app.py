from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
import os
import streamlit as st


# Load environment variables from .env file
load_dotenv()

# Accessing environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")



# @tool
# def multiply(a: int , b: int) ->int:
#   """Multiply a and b. """
#   print("function is called")
#   return a * b

@tool
def calculator(expression: str) -> float:
    """
    Evaluates a given mathematical expression.

    This function takes a mathematical expression as a string, evaluates it, and returns the result.
    It handles basic arithmetic, parentheses, and more complex mathematical calculations.

    Args:
        expression (str): A mathematical expression to evaluate, e.g., "3 + 5 * (2 - 8)".

    Returns:
        Union[float, str]: The result of the evaluated expression, or an error message if invalid.

    Example:
        >>> evaluate_expression("3 + 5 * 2")
        13.0
        >>> evaluate_expression("2 / 0")
        'Error: Division by zero.'
        >>> evaluate_expression("invalid + expression")
        'Error: Invalid input.'
    """
    try:
        # Use eval to compute the result securely
        result = eval(expression, {"__builtins__": None}, {})
        if isinstance(result, (int, float)):  # Ensure result is a number
            return result
        else:
            return "Error: Invalid mathematical expression."
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception:
        return "Error: Invalid input."

tools = [calculator]



llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)
agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

st.title("Gemini Tool Calling")

st.write("welcome to my app")
user_input = st.text_input("Ask any thing")

if st.button("Ask"):
    response = agent.invoke(user_input)
    st.write(response["output"])  # Display the response from the model

