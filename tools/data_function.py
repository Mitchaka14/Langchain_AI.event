# data_function.py

import os
import json
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY


def data_function(question: str) -> str:
    """Answers the given question using a data directory."""

    PERSIST = False
    chat_history = []

    if PERSIST and os.path.exists("persist"):
        vectorstore = Chroma(
            persist_directory="persist", embedding_function=OpenAIEmbeddings()
        )
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = DirectoryLoader("data/")
        if PERSIST:
            index = VectorstoreIndexCreator(
                vectorstore_kwargs={"persist_directory": "persist"}
            ).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    result = chain({"question": question, "chat_history": chat_history})

    chat_history.append((question, result["answer"]))

    # Return the result as a JSON-formatted string.
    return json.dumps(result["answer"])
