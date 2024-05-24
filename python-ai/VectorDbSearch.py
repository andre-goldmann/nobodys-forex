import chromadb
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "all-MiniLM-L6-v2"

load_dotenv()

# TODO refactore all this, so that there is maybe just one method left

def searchWithEf(client, ef, collection_name, query):
    col=client.get_collection(collection_name,embedding_function=ef)
    results = col.query(query_texts=[query])

    #documents = results['documents'][0][0]
    #metadatas = results['metadatas']#[0][0]
    print("found in " + collection_name)
    print(results)

def searchWithSentenceTransformer(client, prompt, collection_name, maxResults = 0):
    collection = client.get_collection(
        name=collection_name
    )
    model = SentenceTransformer(EMBED_MODEL)
    response = model.encode(prompt)

    results = []
    if maxResults > 0:
        results = collection.query(
            query_embeddings=response,
            n_results=maxResults
        )
    else:
        results = collection.query(
            query_embeddings=response
        )

    print("found in " + collection_name)
    print(results)
    #documents = results['documents'][0][0]
    #metadatas = results['metadatas']#[0][0]

    #print(documents)


def searchWithCohere(client, co, prompt, collection_name, maxResults = 3):
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
        n_results=maxResults
    )
    #documents = results['documents'][0][0]
    #metadatas = results['metadatas']#[0][0]
    print("found in " + collection_name)
    print(results)