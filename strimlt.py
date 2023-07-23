import os
import shutil
import sqlite3
import pandas as pd
import streamlit as st
from langchain import LLMMathChain, SerpAPIWrapper, OpenAI, LLMChain
from langchain.agents import (
    AgentType,
    initialize_agent,
    Tool,
)
from langchain.chat_models import ChatOpenAI
from tools.my_tools import DataTool, SQLAgentTool

import subprocess

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

search = SerpAPIWrapper()

data_tool = DataTool()
sql_agent_tool = SQLAgentTool()
sql_agent_tool.description = ""

tools = [
    data_tool,
    sql_agent_tool,
    Tool(
        name="Search",
        func=search.run,
        description="Useful for when you need to ask with search..use for realtime questions like time etc and some internet related things.....",
    ),
]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

db_path = os.path.join(os.getcwd(), "ClinicDb.db")  # The full path of the database file
recovery_db_path = os.path.join(os.getcwd(), "ClinicDbRecovery.db")


# Function to display and edit business info text file
def business_info():
    file_path = os.path.join("data", "business_info.txt")
    with open(file_path, "r+") as file:
        content = file.read()
        updated_content = st.text_area("Business Info:", content)
        if st.button("Save Changes"):
            file.seek(0)
            file.write(updated_content)
            file.truncate()


def get_table_info(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()


def handle_db_upload(uploaded_file):
    if uploaded_file is not None:
        # Check if a database already exists and remove it
        if os.path.exists(db_path):
            os.remove(db_path)

        # Save the uploaded file as the new database
        with open(db_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            st.success("Uploaded file successfully!")

        # Update SQLAgentTool's description
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            sql_agent_tool.description = (
                "Here are the tables and columns available to use:\n"
            )
            for table_name in tables:
                table_name = table_name[0]
                sql_agent_tool.description += f"\nTable: {table_name}\n"
                columns = get_table_info(cursor, table_name)
                sql_agent_tool.description += "Columns:\n" + "\n".join(
                    [column[1] for column in columns]
                )


def display_and_edit_table(conn, table_name):
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    st.dataframe(df)
    st.subheader(f"Edit entries from {table_name}")
    column_to_edit = st.selectbox(
        "Select column to edit", df.columns, key=f"{table_name}_select"
    )
    if column_to_edit:
        entry_to_edit = st.text_input(
            "Enter the entry to edit", key=f"{table_name}_{column_to_edit}_edit"
        )
        new_value = st.text_input(
            "Enter the new value", key=f"{table_name}_{column_to_edit}_value"
        )
        if st.button(
            f"Update {table_name}", key=f"{table_name}_{column_to_edit}_button"
        ):
            query = f"UPDATE {table_name} SET {column_to_edit} = ? WHERE {column_to_edit} = ?"
            try:
                conn.execute(query, (new_value, entry_to_edit))
                conn.commit()
                st.success("Entry updated successfully!")
            except sqlite3.Error as e:
                st.error(f"An error occurred: {e}")


# Function to display and edit database
def database_info():
    uploaded_file = st.file_uploader("Upload a new database (optional)", type="db")
    handle_db_upload(uploaded_file)

    if st.button("Reset"):
        if os.path.exists(db_path):
            os.remove(db_path)
        subprocess.call(["python", "ClinicDb_create.py"])
        sql_agent_tool.description = ""
        st.success("Database reset successfully!")

    if os.path.exists(db_path):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table_name in tables:
                table_name = table_name[0]
                st.subheader(f"Table: {table_name}")
                display_and_edit_table(conn, table_name)


def handle_chat(user_input, system_message):
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


# Streamlit App Starts Here
def main():
    st.title("Customer Service App")
    # Adding navigation
    pages = {
        "Chat": st.empty,
        "Business Info": business_info,
        "Database Info": database_info,
    }
    page = st.sidebar.radio("Navigation", tuple(pages.keys()))
    # Call the function of the selected page
    pages[page]()

    if page == "Chat":
        # Initialize chat history in Session State
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Use a chat input for user input
        user_input = st.chat_input("Enter your message here:")

        # Define the system message
        system_message = """
        system: You are a friendly person named Jack (dont add name in output unless needed)who is a customer service agent. and this conversation is with a customer
        Always make sure users provide thier full name if it has anything to do with appointments or sceduling or most things that should require it 
        """

        # Check if there's user input
        if user_input:
            handle_chat(user_input, system_message)

        # Display the chat history
        for name, message in st.session_state["chat_history"]:
            with st.chat_message(name):
                st.markdown(message)

        # Button to reset conversation
        if st.button("Reset Conversation"):
            st.session_state["chat_history"] = []


if __name__ == "__main__":
    main()
