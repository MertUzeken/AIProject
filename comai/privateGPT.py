from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All
from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA
import time

class privateGPT:

    def __init__(self):
        #Define args
        persist_directory= "db"
        #model_type=str("GPT4All")
        model_type="GPT4All"
        model_path=str("models/ggml-gpt4all-j-v1.3-groovy.bin")
        embeddings_model_name=str("all-MiniLM-L6-v2")
        model_n_ctx=int(1000)
        model_n_batch=int(8)
        target_source_chunks=int(4)

        # Define the Chroma settings
        chroma_settings = Settings(
                chroma_db_impl='duckdb+parquet',
                persist_directory=persist_directory,
                anonymized_telemetry=False
        )
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        db = Chroma(persist_directory=persist_directory,
                     embedding_function=embeddings, 
                     client_settings=chroma_settings
                     )
        
        retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
        
        # activate/deactivate the streaming StdOut callback for LLMs
        callbacksInstance = StreamingStdOutCallbackHandler()
        
        # Prepare the LLM, In Future: Can be used for multiple model "modes"
        match model_type:
                case "GPT4All":
                        self.llm = GPT4All(
                                           model= model_path, 
                                           backend='gptj', 
                                           n_batch=model_n_batch, 
                                           callbacks=None, 
                                           verbose=False
                                           )
                      
                case "other":
                        self.llm = HuggingFaceHub(repo_id="jphme/Llama-2-13b-chat-german-GGML", model_kwargs={"temperature":0.3, "max_length":512})
                case _default:
                        # raise exception if model_type is not supported
                        raise Exception(f"Model type {model_type} is not supported. Please choose one of the following: GPT4All or Your models . . ")
                        
        self.qa = RetrievalQA.from_chain_type(llm=self.llm,
                                                chain_type="stuff",
                                                retriever=retriever,
                                                return_source_documents=True
                                                )

    def sendToGPT(self, query):
        # Get the answer from the chain
        start = time.time()
        res = self.qa(query)
        answer, docs = res['result'], res['source_documents']
        end = time.time()


        remappedDict ={
              "answer": res['result'] ,
              "question": query
        }
        # Print the result
        print("\n\n> Question:")
        print(query)
        print(f"\n> Answer (took {round(end - start, 2)} s.):")
        print(answer)
        return remappedDict

        # Print the relevant sources used for the answer
        print("Mögliche relevante quellen:")
        for document in docs:
            print("\n> " + document.metadata["source"] + ":")
            print(document.page_content)


#gptInstance = privateGPT()
#gptInstance.runQAChain("Wie kann ich meinen Anwesenheitsstatus bei Teams ändern ?")