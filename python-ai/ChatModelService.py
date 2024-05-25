from fastapi import Depends
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import StuffDocumentsChain, LLMChain
from langchain.chains import RetrievalQA
from chromadb import PersistentClient, EmbeddingFunction
from langchain.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from anthropic import Anthropic

class DefChromaEF(Embeddings):
    def __init__(self,ef):
        self.ef = ef

    def embed_documents(self,texts):
        return self.ef(texts)

    def embed_query(self, query):
        return self.ef([query])[0]

async def useChatTemplate():
    chat = ChatCohere(model="command")
    prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
    chain = prompt | chat
    await chain.invoke({"topic": "bears"})

async def talkToCo():

    chat = ChatCohere(model="command")
    #messages = [HumanMessage(content="1"), HumanMessage(content="2 3")]
    messages = [HumanMessage(content="How many people live in Berlin?")]
    chat.invoke(messages)
    #await chat.ainvoke(messages)

    for chunk in chat.stream(messages):
        print(chunk.content, end="", flush=True)

def get_retriever(client: PersistentClient, ef:EmbeddingFunction, collectionName:str,  group_id: str):
    db = Chroma(client=client, collection_name=collectionName,embedding_function=DefChromaEF(ef))
    return db.as_retriever()
    #return db.as_retriever(
    #    search_kwargs={'filter': {
    #        'group_id': group_id
    #    }})

#def get_chain(retriever=Depends(get_retriever)):
def get_chain(retriever):
    # TODO fine tuning: just use data what is in the database
    template = """Answer the question based only on the following context:
    {context}
    If the question can't be answered based on the context, respond with "I don't know."
    Always answer in the language of the question.
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatCohere(model="command")#ChatCohere(api_key=COHERE_API_KEY)
    output_parser = StrOutputParser()

    # Create the LLMChain
    llm_chain = LLMChain(llm=model, prompt=prompt, output_parser=output_parser)

    # Create the StuffDocumentsChain
    stuff_documents_chain = StuffDocumentsChain(llm_chain=llm_chain,
                                                document_variable_name="context")

    # Create the RetrievalQA chain
    chain = RetrievalQA(combine_documents_chain=stuff_documents_chain,
                        retriever=retriever)
    #create_retrieval_chain(combine_documents_chain=stuff_documents_chain,
    #retriever=retriever)#
    return chain


def talkToAntropic(client:Anthropic):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.0,
        system="Respond only in Yoda-speak.",
        #messages=[
        #    {"role": "user", "content": "How are you today?"}
        #]
    )

    print(message.content)