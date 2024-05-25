import uvicorn
from dotenv import load_dotenv
import os

# from fastapi import FastAPI, Request, status, Form
# from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import RequestValidationError
# Bellow the import create a job that will be executed on background
# from fastapi.responses import JSONResponse
# import torch
import chromadb
import cohere
import uvicorn
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
# import spacy
from chromadb.utils.embedding_functions import RoboflowEmbeddingFunction
from chromadb.utils.embedding_functions import InstructorEmbeddingFunction
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Body
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

from VectorDbSearch import searchWithSentenceTransformer, searchWithEf, searchWithCohere
from VectorDbStorage import storeEmbeddings, storeEmbeddings_withEf
from DataLoader import loadFromPdf
from ChatModelService import talkToCo, get_retriever, get_chain, DefChromaEF
import asyncio
from anthropic import Anthropic


CHROMA_DATA_PATH = "chroma_data/"
OLLAME_MODEL_NAME = "phi3"
EMBED_MODEL = "all-MiniLM-L6-v2"
client = PersistentClient(path=CHROMA_DATA_PATH)

load_dotenv()
app = FastAPI()

st_embeddings_collection = 'sentence_transformer_embeddings'
cohere_embeddings_collection = 'cohere_embeddings'
hf_embeddings_collection = 'hf_embeddings_collection'
ollama_embeddings_collection = 'ollama_embeddings_collection'
roboflow_embeddings_collection = 'roboflow_embeddings_collection'

co = cohere.Client(os.environ['COHERE_API_KEY'])
#cohere_ef = CohereEmbeddingFunction(api_key=os.environ['COHERE_API_KEY'],  model_name="large")

roboflow_ef = RoboflowEmbeddingFunction(api_key=os.environ['ROBOFLOW_API_KEY'])

huggingface_ef = HuggingFaceEmbeddingFunction(
    api_key=os.environ['HF_API_KEY'],
    model_name="sentence-transformers/" + EMBED_MODEL
)

ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name=OLLAME_MODEL_NAME,
)

anthropicClient = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ['ANTHROPIC_API_KEY']
)

#instructor_ef = InstructorEmbeddingFunction()

#jinaai_ef = embedding_functions.JinaEmbeddingFunction(
#    api_key="YOUR_API_KEY",
#    model_name="jina-embeddings-v2-base-en"
#)

class ChatData(BaseModel):
    chatbot: str
    query: str

@app.post("/chat/")
async def chat(data: ChatData):
    prompt = [data.query]
    print("Question:")
    print(data.query)

    if data.chatbot == "co":
        retriever = get_retriever(client, ollama_ef, ollama_embeddings_collection,'group_id')
        chain = get_chain(retriever)

        result = chain.invoke(data.query)

        return {"response": result['result']}
    elif data.chatbot == "anthropic":
        #response = anthropicClient.chat(query)
        response = anthropicClient.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.0,
            system="Respond only in Yoda-speak.",
            messages=prompt
            #messages=[
            #    {"role": "user", "content": "How are you today?"}
            #]
        )

        return {"response": response}
    else:
        return {"response": "Chatbot not found"}

# generate a fast api search endpoint
@app.get("/search")
async def search(query: str = Query(None)):
    prompt = [query]

    # TODO there can not be a result searching with 'your_search_term' for example
    # but maybe ther is just a result because of less data or it is necessary to check
    # the distances

    # distances:
    # ollama, cohere:
    # The canine barked loudly.: 0.0, 497.97349744005646, 3384.134136313065, 5151.6243446180415
    # your_search_term: 5396.648604367989, 6143.581355775228, 6238.1581871711915, 6495.914645815324
    # canine barked: 4898.662682687576, 5226.6045583686255, 5821.79239203041, 7517.410092784454
    # check if under 5000 ??

    # Sentence-Transformer, Huggingface:
    # The canine barked loudly.: 5.997904178497418e-13, 0.4462765070947654, 1.7648564175864032, 1.8174345611478135
    # your_search_term: 1.9011532792181667, 1.9245160560863965, 1.936198243474109, 2.0502740882834583
    # canine barked: 0.250512625961966, 0.5532483161489475, 1.7774019871417588, 1.850421385447021
    # -> check if under 1

    print("search for " + query)
    print("###################################")
    searchWithSentenceTransformer(client, prompt, st_embeddings_collection)
    print("###################################") # does not work offline
    searchWithCohere(client, co, prompt, cohere_embeddings_collection)
    print("###################################")
    searchWithEf(client, ollama_ef, ollama_embeddings_collection, query)
    print("###################################")
    searchWithEf(client, roboflow_ef, roboflow_embeddings_collection, query)
    #searchWithOllama(client, ollama_ef([query]), ollama_embeddings_collection)
    #print("###################################") # does not work offline
    # TODO use another model here as this is the same as used by SentenceTransformer
    searchWithEf(client, huggingface_ef, hf_embeddings_collection, query)
    # TODO mistral/claude/alpha a (europ. AI)

    return {"response": "Hello World"}

if __name__ == "__main__":
    refreshData = False
    # Use offline for embeddings
    # Use online for Chat
    #pages = loadFromPdf("icao_hf_guidelines_2003.pdf")
    #print(f"Got {str(len(pages))} pages from document")
    pages = loadFromPdf("PPR_WS_23_24_Abschluss_marked.pdf")
    print(pages[0].page_content)
    #storeEmbeddings_withEf(client, ollama_embeddings_collection, ollama_ef, [pages[0].page_content])
    #for page in pages:
    #    print(page.page_content.replace("\n", " "))
    #vector_index = Chroma.from_documents(documents=pages,
    #                                     #embedding_function=ollama_ef,
    #                                     collection_name=ollama_embeddings_collection,
    #                                     client=client,
    #                                     embedding=DefChromaEF(ollama_ef),
    #                                     persist_directory=CHROMA_DATA_PATH)
    #vector_index.persist()
    #vector_index = Chroma(persist_directory=CHROMA_DATA_PATH,
    #                      embedding_function=DefChromaEF(ollama_ef),
    #                      client=client)
    #https://generativeai.pub/advanced-rag-retrieval-strategy-query-rewriting-a1dd61815ff0
    #https://www.datascienceengineer.com/blog/post-multiple-pdfs-with-gpt
    #chain = get_chain(vector_index.as_retriever())
    retriever = get_retriever(client, ollama_ef, ollama_embeddings_collection,'group_id')
    chain = get_chain(retriever)
    #result = chain.invoke("What is 'An Annex'?")
    result = chain.invoke("Was ist die Abschlussaufgabe?")
    print(result)
    result = chain.invoke("Was sind die nachstehenden Aufgaben?")
    print(result)

    #result = chain.invoke(data.query)

    #asyncio.run(talkToCo())
    # does not work
    #print(roboflow_ef(input=loadFromPdf()))
    # does not work
    #print(instructor_ef(loadFromPdf()))
    #jinaai_ef(input=["This is my first text to embed", "This is my second document"])
    if refreshData:
        if st_embeddings_collection in [c.name for c in client.list_collections()]:
            client.delete_collection(name=st_embeddings_collection)
        if cohere_embeddings_collection in [c.name for c in client.list_collections()]:
                    client.delete_collection(name=cohere_embeddings_collection)
        if hf_embeddings_collection in [c.name for c in client.list_collections()]:
            client.delete_collection(name=hf_embeddings_collection)
        if ollama_embeddings_collection in [c.name for c in client.list_collections()]:
            client.delete_collection(name=ollama_embeddings_collection)
        if roboflow_embeddings_collection in [c.name for c in client.list_collections()]:
            client.delete_collection(name=roboflow_embeddings_collection)

        texts = loadFromPdf("icao_hf_guidelines_2003.pdf")
        storeEmbeddings_withEf(client, roboflow_embeddings_collection, roboflow_ef, texts)
        # print("Run Spacy")
        #nlp = spacy.load("en_core_web_md")
        #spacy_embeddings = nlp.vocab[texts].vector

        print("Run SentenceTransformer")
        model = SentenceTransformer(EMBED_MODEL)
        st_embeddings = model.encode(texts)
        # does not work
        storeEmbeddings(client, st_embeddings_collection, st_embeddings, texts)

        #print("Run Cohere")
        cohere_embeddings = co.embed(texts=texts,
                       model='large',
                       input_type="search_documents",
                       embedding_types=['float']
                      )

        storeEmbeddings(client, cohere_embeddings_collection, cohere_embeddings.embeddings.float_, texts)

        #print("Run HF")
        storeEmbeddings_withEf(client, hf_embeddings_collection, huggingface_ef, texts)

        print("Run Ollama")
        storeEmbeddings_withEf(client, ollama_embeddings_collection, ollama_ef, texts)


    #print("Found colllections:")
    #for c in client.list_collections():#
    #    print(c)

    #searchWithSentenceTransformer(client, prompt, st_embeddings_collection)
    #searchWithCohere(client, prompt, cohere_embeddings_collection)
    #does not work
    #roboflow_ef(texts)
    #does not work
    #storeEmbeddings_withef(cohere_embeddings_collection, roboflow_ef, texts)

    uvicorn.run(app, host="0.0.0.0", port=80)