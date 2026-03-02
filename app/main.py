from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import os
import shutil

from app.trainer import train_model
from app.predictor import load_model, predict_message

app = FastAPI(title="Message Trust AI Platform")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
os.makedirs(os.path.join(os.path.dirname(__file__), "models"), exist_ok=True)

class MessageItem(BaseModel):
    id: str
    content: str

class AnalyzeRequest(BaseModel):
    messages: List[MessageItem]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/train", response_class=HTMLResponse)
def train_page(request: Request):
    return templates.TemplateResponse("train.html", {"request": request})

@app.post("/train")
async def upload_and_train(file: UploadFile = File(...)):
    file_path = os.path.join(os.path.dirname(__file__), "models", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    train_model(file_path)

    return {
        "status": "Model trained successfully",
        "model": "clear_sender_model.bin",
    }

@app.get("/test", response_class=HTMLResponse)
def test_page(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.post("/predict")
async def predict(text: str = Form(...)):
    model = load_model()
    if not model:
        return {"error": "Model not trained yet. Please train first."}

    if not text.strip():
        return {"error": "Message text is empty."}

    return predict_message(model, text)

@app.post("/analyze")
async def analyze_messages(req: AnalyzeRequest):
    model = load_model()
    if not model:
        return {"error": "Model not trained yet. Please train first."}
    
    results = []
    for msg in req.messages:
        if not msg.content.strip():
            pred = {"error": "Message content is empty."}
        else:
            pred = predict_message(model, msg.content)
            
        results.append({
            "id": msg.id,
            "content": msg.content,
            "prediction": pred
        })
        
    return {"results": results}
