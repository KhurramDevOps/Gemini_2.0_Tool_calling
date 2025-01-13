from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
import os
import streamlit as st

from tools import  calculator,get_distance,get_stock_price,get_weather,latest_news,google_search_tool

# Load environment variables from .env file
load_dotenv()

# Accessing environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")



# @tool
# def multiply(a: int , b: int) ->int:
#   """Multiply a and b. """
#   print("function is called")
#   return a * b


tools = [calculator,latest_news,get_stock_price,get_weather,google_search_tool,get_distance]



llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)
agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

st.set_page_config(page_title="Practice Tool Calling App", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for more styling
st.markdown(
    """
    <style>
    body {
        background-color: white;
        font-family: 'Arial', sans-serif;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        border-radius: 8px;
        width : 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ccc;
        width: 100%;
    }
    .sidebar .sidebar-content {
        background-color: #e0f7fa;
        font-size: 18px;
        font-weight: bold;
    }
    h1 {
        color: #333;
        font-size: 40px;
        text-align: center;
    }
    h2 {
        color: #555;
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title of the app
st.title("AI-Powered Tool Assistant 🤖")

# Sidebar for navigation
st.sidebar.title("Available Tools")
tools = [calculator,
         latest_news,
         get_stock_price,
         get_weather,
         google_search_tool,
         get_distance]



for tool in tools:
    st.sidebar.write(f"- {tool.name}")


# Add a brief description on the main page
st.markdown("""
    <h2>Welcome to the AI-Powered Tool Assistant 🤖</h2>
    <p>This app uses a powerful language model to help you access various tools. 
    Simply type your question below and let the app automatically select the right tool for you!</p>
""", unsafe_allow_html=True)

# Text input for user to ask a question
user_input = st.text_input("Ask anything", placeholder="Type your question here...")

# Button for submission
if st.button("Submit"):
    # Pass the user input to your LLM to decide the appropriate tool and generate a response
    result = agent.invoke({"input": user_input})
    
    # Display the result from the LLM
    st.write(result["output"])






# # Button to start listening
# if st.button("Start Speaking"):
#     with st.spinner("Listening..."):
#         handle_audio_input(tool_input="start")

