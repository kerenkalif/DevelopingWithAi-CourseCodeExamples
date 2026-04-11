from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from chain import ask_assistant

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class AssistantRequest(BaseModel):
    role:     str
    question: str


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/ask")
def ask(request: AssistantRequest):
    try:
        answer = ask_assistant(request.role, request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
