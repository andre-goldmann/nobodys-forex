from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def loadFromPdf(fileName:str):

    loader = PyPDFLoader(f"./data/{fileName}")
    pages_1 = loader.load()

    #Each page is a Document. A Document contains text (page_content) and metadata.
    #print("Pages loaded: " + str(len(pages_1)))
    print(f"{loader.file_path} contais {str(len(pages_1))} pages")
    page = pages_1[0]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return loader.load_and_split(text_splitter)


    #print(page.page_content)
    #print(len(pages_1))

    #return [
    #    "The canine barked loudly.",
    #    "The dog made a noisy bark.",
    #    "He ate a lot of pizza.",
    #    "He devoured a large quantity of pizza pie.",
    #]

def loadDFromCsv():
    return ["CSV-Content"]

def loadFromDb():
    return ["DB-Content"]