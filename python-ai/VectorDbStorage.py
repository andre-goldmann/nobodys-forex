import uuid
from chromadb import PersistentClient, EmbeddingFunction


def storeEmbeddings(
        client:PersistentClient,
        collectionName:str,
        embeddings,
        documents,
        get_or_create: bool = False):
    print(f"Size embedding-0 = {len(embeddings[0])}")

    collection = client.create_collection(
        name=collectionName,
        get_or_create=get_or_create
        #metadata={"hnsw:space": "cosine"},
    )
    # TODO embeddings are None at the moment
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[str(uuid.uuid4()) for _ in range(len(documents))],
    )
    count = collection.count()
    print("Embedding stored for to " + collectionName)
    print("Contains now " + str(count) + " documents!")


def storeEmbeddings_withEf(
        client:PersistentClient,
        collectionname:str,
        ef:EmbeddingFunction,
        documents,
        get_or_create: bool = False):
    collection = client.create_collection(name=collectionname, embedding_function=ef, get_or_create=get_or_create)
    collection.add(
        documents=documents,
        #metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=[str(uuid.uuid4()) for _ in range(len(documents))]
    )