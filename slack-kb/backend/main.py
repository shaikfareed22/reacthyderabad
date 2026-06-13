import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

os.environ["AQ.Ab8RN6KtUTnP49BoMjkfAmIFRIcb5W0v8bwtvkCg3WbNx5arqw"] = "AQ.Ab8RN6KtUTnP49BoMjkfAmIFRIcb5W0v8bwtvkCg3WbNx5arqw"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

vectordb = None

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global vectordb
    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    loader = PyPDFLoader(path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma.from_documents(chunks, embeddings)

    os.remove(path)
    return {"status": "success", "chunks": len(chunks)}

@app.post("/ask")
async def ask(question: str):
    if vectordb is None:
        return {"answer": "Please upload a document first.", "sources": []}

    docs = vectordb.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    prompt = f"Answer based on this context:\n{context}\n\nQuestion: {question}"
    response = llm.invoke(prompt)

    sources = [{"page": d.metadata.get("page", "N/A"), "snippet": d.page_content[:150]} for d in docs]
    return {"answer": response.content, "sources": sources}

@app.get("/")
def home():
    return {"status": "Backend running"}
