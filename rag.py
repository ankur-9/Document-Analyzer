from langchain_core.tools import retriever
from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains import RetrievalQAWithSourcesChain
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()


CHUNK_SIZE = 200
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate"

llm = None
vector_store = None

def initialize_components():
    global llm, vector_store

    if llm is None:
        llm = ChatGroq(model="llama-3.3-70b-versatile",
                       temperature=0.9,
                       max_tokens=1000
                       )
    if vector_store is None:

        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        vector_store = Chroma(collection_name = COLLECTION_NAME,
               embedding_function = ef,
               persist_directory = str(VECTORSTORE_DIR)
               )

def process_urls(urls):
    """
    This function scraps data from urls and stores it in vector db
    :param urls:
    :return:
    """

    print("Initialize components")
    initialize_components()
    vector_store.reset_collection()

    print("Load Data")
    loader = SeleniumURLLoader(urls)
    data = loader.load()

    print("Split texts")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=20
    )
    docs = text_splitter.split_documents(data)

    print("Add docs to vector db")
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs,ids = uuids)
    print("Added docs to vector db")


def generate_answers(query):

    if not vector_store:
        raise RuntimeError("Vector database is not initialized")

    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context.
    If you don't know the answer, just say you don't know.
    
    Context:
    {context}
    
    Question: {question}
    """)

    retriever = vector_store.as_retriever()
    chunks = retriever.invoke(query)

    sources = list(set(c.metadata.get("source","") for c in chunks))
    formatted_context = "\n\n".join(c.page_content for c in chunks)

    rag_chain = (
        {"context":RunnablePassthrough(), "question":RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke({"context":formatted_context,"question":query})
    return answer,sources


if __name__ == "__main__":

    urls = ["https://www.ign.com/articles/forza-horizon-6-review",
            "https://www.ign.com/wikis/forza-horizon-6/Tips_and_Tricks_-_Everything_to_Know_Before_Playing",
            "https://www.ign.com/wikis/forza-horizon-6/Best_Starter_Car"]

    process_urls(urls)

    # results = vector_store.similarity_search(
    #     "30 year mortgage rate",
    #     k=2
    # )
    # print(results)

    answer, sources = generate_answers("What are some of the best starter cars in Forza Horizon 6 and why?")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")