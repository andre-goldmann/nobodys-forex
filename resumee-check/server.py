import logging
import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import pandas as pd
import asyncio
import uuid
import ollama

CHROMA_DATA_PATH = "chroma_data/"
COLLECTION_NAME = "demo_docs"
MODEL_NAME = "phi3"


class UserData(BaseModel):
    firstname: str
    lastname: str
    job_title: str
    state: str
    email: str
    linkedprofil: str
    resumee: str


ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name=MODEL_NAME,
)
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

app = FastAPI()

@app.get("/check/")
async def check(jobtitle: str = Query(description="The job title"),
                jobdescription: str = Query(None, description="The job description")):
    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    #question='having the following Job description:'
    prompt = [jobtitle]
    if jobdescription is not None:
        prompt.append(jobdescription)
    else:
        #https://github.com/ollama/ollama-python
        print("TODO search for a job description")
        response = ollama.chat(model=MODEL_NAME, messages=[
            {
                'role': 'user',
                'content': 'description position ' + jobtitle,
            },
        ])
        # TODO add this to another collection called jobdescription
        #print(response['message']['content'])
        prompt.append(response['message']['content'].replace("\n","").replace("\n-",""))

        #prompt.append("")
    print("Search for:")
    print(prompt)

    response = ollama_ef(prompt)

    results = collection.query(
        query_embeddings=response,
        n_results=3
    )
    #documents = results['documents'][0][0]
    metadatas = results['metadatas']#[0][0]
    # TODO here ask Chat
    # having the jobtitle x and the jobdescription x what of the following resumees matches best
    return {"result": metadatas}


@app.post("/adduser/")
async def create_user(user_data: UserData):

    print("firstname=" + user_data.firstname + ", lastname=" + user_data.lastname + ", state=" + user_data.state + ", email=" + user_data.email + ", linkedprofil=" + user_data.linkedprofil + ", resumee=" +user_data.resumee)
    texts = [user_data.resumee]
    embeddings = ollama_ef(texts)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )
    collection.add(
         #documents=texts,
         embeddings=embeddings,
         ids=[str(uuid.uuid4())],
         metadatas=[user_data.dict()]
     )

    return {"message": "User created successfully"}


if __name__ == "__main__":
    refreshData = True
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if refreshData:
        if COLLECTION_NAME in [c.name for c in client.list_collections()]:
            client.delete_collection(name=COLLECTION_NAME)

        df = pd.read_csv('data.csv', sep=';')

        for index, row in df.iterrows():
            user_data = UserData(
                firstname=row[0].replace("'", ""),
                lastname=row[1].replace("'", ""),
                job_title=row[2].replace("'", ""),
                state=row[3].replace("'", ""),
                email=row[5].replace("'", ""),
                linkedprofil=row[7].replace("'", ""),
                resumee=row[10].replace("Objective: ", "").replace("'", "")
            )

            asyncio.run(create_user(user_data))

    uvicorn.run(app, host="0.0.0.0", port=80)