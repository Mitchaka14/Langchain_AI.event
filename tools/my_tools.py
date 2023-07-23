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
    This tool provides information about the bussiness. 
    it has the bussiness name and other bussiness related stuff,if its not here then Search
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
    name = "ClinicDBTool"
    description = """
    This tool interacts with a Clinic SQL database, facilitating operations related to patients, appointments, employees, and related medical records,availability.
    With this tool, you can:
        - Create, update, and retrieve details about patients, employees, and appointments.
        - Create and fetch related data such as prescriptions, test results, billing information, complaints, referrals, and interactions.
    If the input is a patient or employee name, it retrieves all related information. This tool also enables creating new entries in the database when needed, a new or existing patient name is needed .
    Don't give patients information they shoould and dont need to know
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


# class InteractiveTool(BaseTool):
#     class Config:
#         extra = Extra.allow

#     name = "InteractiveTool"
#     description = """
#     This tool interacts with the user, allowing the system to ask for additional information.
#     Tool selection after...call custom_dataTool if it is Business related,
#     call Appointments/scheduler if its Appointments/scheduler related, etc.
#     dont end conversation unless, the customer is satisfied
#     """

#     def __init__(self, event_handler):
#         super().__init__()
#         self.event_handler = event_handler

#     def _run(
#         self,
#         query: Optional[str] = None,
#         run_manager: Optional[CallbackManagerForToolRun] = None,
#     ) -> str:
#         """Use the tool."""
#         return self.event_handler("input_required", query if query else "Enter input: ")

#     async def _arun(
#         self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
#     ) -> str:
#         """Use the tool asynchronously."""
#         # The input function is not compatible with asynchronous programming.
#         raise NotImplementedError("InteractiveTool does not support async")


# class FeedbackTool(BaseTool):
#     name = "FeedbackTool"
#     description = """
#     This tool should be called last,or  InteractiveTool can be called after if you ask a question
#     use this tool to determine if you should end the chain or you should ask the customer if the have more question.

#     """

#     def _run(
#         self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
#     ) -> str:
#         """Use the tool."""
#         return f"""
#                     agent input was: {query}. Ask customer if they satisfied?(if they are end the chain), Do you still need help?(if they do provide the help)
#                     InteractiveTool use that tool next if you are asking the customer a question, or end conversation if you are saying goodbye
#                     """

#     async def _arun(
#         self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
#     ) -> str:
#         """Use the tool asynchronously."""
#         raise NotImplementedError("FeedbackTool does not support async")
