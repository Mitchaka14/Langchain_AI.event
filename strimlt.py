import streamlit as st
import os
import json
from langchain import LLMMathChain, SerpAPIWrapper, OpenAI, LLMChain
from langchain.agents import (
    AgentType,
    initialize_agent,
    Tool,
    ZeroShotAgent,
    AgentExecutor,
)
from langchain.chat_models import ChatOpenAI
from tools.my_tools import DataTool, SQLAgentTool
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.chains import ConversationChain
from langchain.output_parsers import OutputFixingParser, DefaultOutputParser
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
        description="useful for when you need to ask with search......dont end conversation unless, the customer is satisfied",
    ),
]

prefix = """dont end conversation unless, the customer is satisfied
You are a customer service agent named Jack. You are friendly but firm and don't let customers make unnecessary changes to the database.
If they want to make changes, you have to confirm with their name if it's them.
You don't end the conversation until the user is either satisfied or wants to leave.
always confirm before ending the conversation, follow proper etiquette
You have access to the following tools:"""
suffix = """Begin!   

{chat_history}
CustomerInput: {input}
dont end conversation unless, the customer is satisfied"
{agent_scratchpad}
dont end conversation unless, the customer is satisfied"
"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"), prompt=prompt
)

# Create an instance of the original parser
original_output_parser = DefaultOutputParser()

# Create an instance of the output fixing parser
output_fixing_parser = OutputFixingParser(original_output_parser, llm_chain.llm)

agent = ZeroShotAgent(
    llm_chain=llm_chain,
    tools=tools,
    verbose=True,
    memory=memory,
    output_parser=output_fixing_parser,  # Use the fixing parser here
)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory, max_iterations=1000
)


# Streamlit App Starts Here

st.title("Customer Service App")

# Initialize chat history in Session State
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Use a chat input for user input
user_input = st.chat_input("Enter your message here:")

# Check if there's user input
if user_input:
    # Add user input to chat history
    st.session_state["chat_history"].append(("user", user_input))

    # Run the agent
    output = agent_chain.run(input=user_input)

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
    memory.reset()
    st.session_state["chat_history"] = []
