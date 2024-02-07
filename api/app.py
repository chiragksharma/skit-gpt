import os
from dotenv import load_dotenv
from fastapi import FastAPI, responses
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from embedchain import Pipeline
import uvicorn

load_dotenv(".env")

app = FastAPI(title="Embedchain FastAPI App")
embedchain_app = Pipeline()
origins = [
   
    "*",  # Allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Specify allowed methods
    allow_headers=["X-Requested-With", "Content-Type", "Authorization"],  # Specify allowed headers
)
embedchain_app.add("https://www.skit.ac.in", data_type='web_page')
embedchain_app.add("https://www.skit.ac.in/index.php?option=com_schuweb_sitemap&view=xml&tmpl=component&id=1", data_type='sitemap')
embedchain_app.add("https://www.skit.ac.in/faculty-it.html", data_type='web_page')
embedchain_app.add('https://www.skit.ac.in/faculty-cse.html', data_type='web_page')
embedchain_app.add('https://www.skit.ac.in/images/cs-files/cse_faculty_list_2022-23.pdf')
embedchain_app.add('https://www.skit.ac.in/faculty-ce.html', data_type='web_page')
embedchain_app.add('https://www.skit.ac.in/examination-cell.html', data_type='web_page')
embedchain_app.add('https://www.skit.ac.in/noticess.html',data_type='web_page')



class SourceModel(BaseModel):
    source: str


class QuestionModel(BaseModel):
    question: str


@app.post("/add")
async def add_source(source_model: SourceModel):
    """
    Adds a new source to the EmbedChain app.
    Expects a JSON with a "source" key.
    """
    source = source_model.source
    embedchain_app.add(source)
    return {"message": f"Source '{source}' added successfully."}


@app.post("/query")
async def handle_query(question_model: QuestionModel):
    """
    Handles a query to the EmbedChain app.
    Expects a JSON with a "question" key.
    """
    question = question_model.question
    answer = embedchain_app.query(question)
    return {"answer": answer}


@app.post("/chat")
async def handle_chat(question_model: QuestionModel):
    """
    Handles a chat request to the EmbedChain app.
    Expects a JSON with a "question" key.
    """
    question = question_model.question
    response = embedchain_app.query(question)
    return {"response": response}


@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")

if __name__ == '__main__':
    uvicorn.run(port=5000,host="0.0.0.0")
