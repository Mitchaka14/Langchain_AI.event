# my_tools.py

from typing import Optional, Type
from pydantic import BaseModel
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from typing import Optional, Type
from pydantic import BaseModel, Extra
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun


class DataInput(BaseModel):
    question: str


class DataTool(BaseTool):
    name = "custom_dataTool"
    description = """ 
    This tool provides information on queries about the bussiness.
    be more specific with the query , 
    if i cant reply without more context then reform the question 
    also if i dont have the answer use the bussiness information to search for the answer with search tool
    dont end conversation unless, the customer is satisfied
    ...
    """
    # args_schema: Type[BaseModel] = DataInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        from .data_function import (
            data_function,
        )  # Import the function here to avoid circular imports

        output = data_function(query)
        return output

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("/data does not support async")


class SQLAgentInput(BaseModel):
    query: str


class SQLAgentTool(BaseTool):
    name = "Appoinments/scheduler"
    description = """
    This tool interacts with a SQL database, answering questions about the Appointments, and setting new appoinments.,
    This tool will create new entries in the database if needed
    if the input is just a name then retrieve info about the name either 1 of the names or the full name 
    dont end conversation unless, the customer is satisfied
    """
    args_schema: Type[BaseModel] = SQLAgentInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        from .sql_agent_function import (
            sql_agent_function,
        )  # Import the function here to avoid circular imports

        output = sql_agent_function(query)
        return output

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("/SQLAgentTool does not support async")


class InteractiveTool(BaseTool):
    class Config:
        extra = Extra.allow

    name = "InteractiveTool"
    description = """
    This tool interacts with the user, allowing the system to ask for additional information.
    Tool selection after...call custom_dataTool if it is Business related, 
    call Appointments/scheduler if its Appointments/scheduler related, etc.
    dont end conversation unless, the customer is satisfied
    """

    def __init__(self, event_handler):
        super().__init__()
        self.event_handler = event_handler

    def _run(
        self,
        query: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return self.event_handler("input_required", query if query else "Enter input: ")

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        # The input function is not compatible with asynchronous programming.
        raise NotImplementedError("InteractiveTool does not support async")


class FeedbackTool(BaseTool):
    name = "FeedbackTool"
    description = """
    This tool should be called last,or  InteractiveTool can be called after if you ask a question
    use this tool to determine if you should end the chain or you should ask the customer if the have more question.

    """

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return f"""
                    agent input was: {query}. Ask customer if they satisfied?(if they are end the chain), Do you still need help?(if they do provide the help)
                    InteractiveTool use that tool next if you are asking the customer a question, or end conversation if you are saying goodbye
                    """

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("FeedbackTool does not support async")
