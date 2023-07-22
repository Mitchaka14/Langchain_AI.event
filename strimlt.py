# strimlt.py
import os
import streamlit as st
from langchain import LLMMathChain, SerpAPIWrapper, OpenAI, LLMChain
from langchain.agents import (
    AgentType,
    initialize_agent,
    Tool,
)
from langchain.chat_models import ChatOpenAI
from tools.my_tools import DataTool, SQLAgentTool
import constants

# Setting up environment variables
os.environ["OPENAI_API_KEY"] = constants.APIKEY
os.environ["serpapi_api_key"] = constants.SERPAPI_API_KEY

search = SerpAPIWrapper()

tools = [
    DataTool(),
    SQLAgentTool(),
    Tool(
        name="Search",
        func=search.run,
        description="Useful for when you need to ask with search. Don't end conversation unless the customer is satisfied.",
    ),
]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

# Streamlit App Starts Here
st.title("Customer Service App")

# Initialize chat history in Session State
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Use a chat input for user input
user_input = st.chat_input("Enter your message here:")

# Define the system message
system_message = "system: You are a friendly person named Jack (dont add name in output unless needed)who is a customer service agent. and this conversation is with a customer"

# Check if there's user input
if user_input:
    # Add user input to chat history
    st.session_state["chat_history"].append(("user", user_input))

    # Format the input to agent.run()
    formatted_input = "\n".join(
        [system_message]
        + [f"{name}: {message}" for name, message in st.session_state["chat_history"]]
    )

    # Run the agent
    output = agent.run(input=formatted_input)

    # Extract agent response from output
    agent_response = output.split("Final Answer:")[-1].strip()

    # Add agent response to chat history
    st.session_state["chat_history"].append(("assistant", agent_response))

# Display the chat history
for name, message in st.session_state["chat_history"]:
    with st.chat_message(name):
        st.markdown(message)

# Button to reset conversation
if st.button("Reset Conversation"):
    st.session_state["chat_history"] = []
