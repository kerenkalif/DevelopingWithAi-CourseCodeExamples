import uuid
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from chain import ask_assistant

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

sessions: dict[str, list[dict]] = {}


class StartRequest(BaseModel):
    role: str


class AssistantRequest(BaseModel):
    session_id: str
    question:   str


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/start")
def start(request: StartRequest):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"role": request.role, "history": []}
    return {"session_id": session_id}


@app.post("/ask")
def ask(request: AssistantRequest):
    session = sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        answer = ask_assistant(session["role"], request.question, session["history"])
        session["history"].append({"question": request.question, "answer": answer})
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
