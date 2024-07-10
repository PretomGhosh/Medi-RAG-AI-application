from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema.messages import HumanMessage
from langchain.schema.document import Document
from langchain_community.vectorstores import FAISS
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from dotenv import load_dotenv
from langchain import LLMChain

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = os.getenv('OPENAI_API_KEY')
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

prompt_template = """You are a vet doctor and an expert in analyzing dog's health.
Answer the question based only on the following context, which can include text, images and tables:
{context}
Question: {question}
Don't answer if you are not sure and decline to answer and say "Sorry, I don't have much information about it."
Just return the helpful answer in as much as detailed possible.
Answer:
"""

qa_chain = LLMChain(
    llm=ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key, max_tokens=1024),
    prompt=PromptTemplate.from_template(prompt_template)
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_answer")
async def get_answer(question: str = Form(...)):
    try:
        logging.info(f"Received question: {question}")
        relevant_docs = db.similarity_search(question)
        logging.info(f"Retrieved {len(relevant_docs)} relevant documents.")
        
        context = ""
        relevant_images = []
        for d in relevant_docs:
            if d.metadata['type'] == 'text':
                context += '[text]' + d.metadata['original_content']
            elif d.metadata['type'] == 'table':
                context += '[table]' + d.metadata['original_content']
            elif d.metadata['type'] == 'image':
                context += '[image]' + d.page_content
                relevant_images.append(d.metadata['original_content'])
        
        logging.info(f"Context: {context}")
        logging.info(f"Relevant images: {relevant_images}")

        result = qa_chain.run({'context': context, 'question': question})
        logging.info(f"Generated answer: {result}")
        
        return JSONResponse({"relevant_images": relevant_images[0] if relevant_images else "", "result": result})
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
