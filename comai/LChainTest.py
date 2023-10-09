from chromadb.config import Settings
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
import ingestgpt4all

#Info: This version of LChain uses ChromaDB (ingestcomai.py) to create vectordb with OpenAI Embeddings.
class comai:

    def __init__(self):
        #Define args
        persist_directory= "db" 
        os.environ["OPENAI_API_KEY"] = ("")
        self.chat_history = []


        # Define the Chroma settings
        chroma_settings = Settings(
                chroma_db_impl='duckdb+parquet',
                persist_directory=persist_directory,
                anonymized_telemetry=False
        )

        #Setup the rest
        embeddings = OpenAIEmbeddings()
        self.db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=chroma_settings)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.pdf_qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.05, model_name="text-davinci-003") , self.db.as_retriever(), memory=self.memory)
        

    def setupIngestion():
        ingestgpt4all.embeddings_model_name = "text-embedding-ada-002"

    def sendToGPT(self, query):
        result = self.pdf_qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.append((query, result['answer']))
        print(result['answer'])   
        return result

#vvvvv  uncomment for test vvvvv 
#instance = comai()
#instance.sendToGPT("Wie kann ich meinen Anwesenheitsstatus in Teams ändern ?")
