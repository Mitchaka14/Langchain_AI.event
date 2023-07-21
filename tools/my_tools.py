# my_tools.py

from typing import Optional, Type
from pydantic import BaseModel
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from typing import Optional, Type
from pydantic import BaseModel
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
    if the input is just a name then retrieve info about the name either 1 of the names or the full name 
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
    name = "InteractiveTool"
    description = """
    This tool interacts with the user, allowing the system to ask for additional information.tool selection after...call custom_dataTool if it is Bussiness related, call Appoinments/scheduler if its Appoinments/scheduler related, etc 
    """

    def _run(
        self,
        query: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        response = input(query if query else "Enter input: ")
        return response

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        # The input function is not compatible with asynchronous programming.
        raise NotImplementedError("InteractiveTool does not support async")
