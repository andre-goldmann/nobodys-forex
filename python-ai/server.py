import logging
import uvicorn
from dotenv import load_dotenv
import os
#from fastapi import FastAPI, Request, status, Form
#from fastapi.encoders import jsonable_encoder
#from fastapi.exceptions import RequestValidationError
# Bellow the import create a job that will be executed on background
#from fastapi.responses import JSONResponse
from transformers import AutoModelForCausalLM, AutoTokenizer
#import torch
import chromadb
from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import spacy
from chromadb.utils.embedding_functions import CohereEmbeddingFunction
from chromadb.utils.embedding_functions import RoboflowEmbeddingFunction
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import ollama
import cohere

CHROMA_DATA_PATH = "chroma_data/"
OLLAME_MODEL_NAME = "phi3"
EMBED_MODEL = "all-MiniLM-L6-v2"
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

load_dotenv()
app = FastAPI()

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

from transformers import T5ForConditionalGeneration, T5Tokenizer

#def load_model():
#    model = T5ForConditionalGeneration.from_pretrained('castorini/doc2query-t5-base-msmarco')
#    tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
#    return model, tokenizer

#def process_data(text, model, tokenizer):
#    # Prepare the input text
#    input_text = f"generate query: {text}"
#    # Encode the input text
#    input_ids = tokenizer.encode(input_text, return_tensors='pt')
#    # Generate the output
#    output = model.generate(input_ids, max_length=25, num_return_sequences=1)
#    # Decode the output
#    response = tokenizer.decode(output[0], skip_special_tokens=True)
#    return response



def storeEmbeddings(collectionName, embeddings, documents):

    collection = client.create_collection(
        name=collectionName,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[f"id{i}" for i in range(len(documents))]
    )
    count = collection.count()
    print("Embedding stored for to " + collectionName)
    print("Contains now " + str(count) + " documents!")


def storeEmbeddings_withef(collectionname, ef, documents):
    huggingface_collection = client.create_collection(name=collectionname, embedding_function=ef)
    huggingface_collection.add(
        documents=documents,
        #metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=[f"id{i}" for i in range(len(documents))]
    )


def searchWithSentenceTransformer(prompt, collection_name):
    collection = client.get_collection(
        name=collection_name
    )
    model = SentenceTransformer(EMBED_MODEL)
    response = model.encode(prompt)

    results = collection.query(
        query_embeddings=response,
        n_results=3
    )
    documents = results['documents'][0][0]
    #metadatas = results['metadatas']#[0][0]
    print("found in " + collection_name)
    print(documents)


def searchWithCohere(prompt, collection_name):
    #see also https://docs.pinecone.io/integrations/cohere
    cohere_embeddings = co.embed(texts=prompt,
                                 model='large',
                                 input_type="search_query",
                                 embedding_types=['float'],
                                 truncate='END'
                                 )

    collection = client.get_collection(
        name=collection_name
    )
    results = collection.query(
        query_embeddings=cohere_embeddings.embeddings.float_,
        n_results=3
    )
    documents = results['documents'][0][0]
    #metadatas = results['metadatas']#[0][0]
    print("found in " + collection_name)
    print(documents)


if __name__ == "__main__":
    refreshData = False
    st_embeddings_collection = 'sentence_transformer_embeddings'
    cohere_embeddings_collection = 'cohere_embeddings'
    hf_embeddings_collection = 'hf_embeddings_collection'
    if refreshData:
        if st_embeddings_collection in [c.name for c in client.list_collections()]:
            client.delete_collection(name=st_embeddings_collection)
        if cohere_embeddings_collection in [c.name for c in client.list_collections()]:
                    client.delete_collection(name=cohere_embeddings_collection)
        if hf_embeddings_collection in [c.name for c in client.list_collections()]:
            client.delete_collection(name=hf_embeddings_collection)

        texts = [
                "The canine barked loudly.",
                "The dog made a noisy bark.",
                "He ate a lot of pizza.",
                "He devoured a large quantity of pizza pie.",
            ]
        # print("Run Spacy")
        #nlp = spacy.load("en_core_web_md")
        #spacy_embeddings = nlp.vocab[texts].vector

        print("Run SentenceTransformer")
        model = SentenceTransformer(EMBED_MODEL)
        st_embeddings = model.encode(texts)

        storeEmbeddings(st_embeddings_collection, st_embeddings, texts)

        print("Run Cohere")
        cohere_embeddings = co.embed(texts=texts,
                       model='large',
                       input_type="search_documents",
                       embedding_types=['float']
                      )

        storeEmbeddings(cohere_embeddings_collection, cohere_embeddings.embeddings.float_, texts)

        print("Run HF")
        storeEmbeddings_withef(hf_embeddings_collection, huggingface_ef, texts)

    #print("Found colllections:")
    #for c in client.list_collections():#
    #    print(c)

    ### Search
    prompt = ["What is canine?"]
    #response = ollama_ef(prompt)

    searchWithSentenceTransformer(prompt, st_embeddings_collection)
    searchWithCohere(prompt, cohere_embeddings_collection)
    #does not work
    #roboflow_ef(texts)
    #does not work
    #storeEmbeddings_withef(cohere_embeddings_collection, roboflow_ef, texts)

    #uvicorn.run(app, host="0.0.0.0", port=80)