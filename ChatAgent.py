# main.py

import os
import json
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from tools.my_tools import DataTool, SQLAgentTool, InteractiveTool

import constants


def get_user_input(prompt):
    return input(prompt)


os.environ["OPENAI_API_KEY"] = constants.APIKEY
os.environ["serpapi_api_key"] = constants.SERPAPI_API_KEY
# Initialize the LLM to use for the agent.
llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo-0613")
search = SerpAPIWrapper()
# Construct the agent.
tools = [
    DataTool(),
    SQLAgentTool(),
    InteractiveTool(),
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to ask with search",
    ),
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    get_user_input=get_user_input,  # Pass your function as a callback
)
initialPrompt = """
((prompt)You are customer service agent named jack, you are friendly but firm and doesnt let customers make unnesesarry changes to the database
if they want to make changes you have to confirm with thier name if its them
You are interacting with a customer....dont end the conversation till the user is either satisfied or wants to leave(prompt)  )input>>
"""
json_output = agent.run(initialPrompt + "what are my appointments ")

# Print the JSON output. Depending on the structure of your JSON, you might want to parse it into a Pydantic model, as I showed in the previous examples.
print(json_output)
