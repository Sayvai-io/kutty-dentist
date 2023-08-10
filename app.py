# app.py
import uvicorn
from fastapi import FastAPI,Form
from pydantic import BaseModel
# to avoid CORS errors when running locally
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from llm import Server
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import File, UploadFile
from whisperaudio import get_text
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


origins = [
    "http://localhost",
    "http://localhost:8080",
]
# cors middleware



app = FastAPI(
    title = "Server-LLM",
    version = '0.0.1'
)

account_sid = 'ACfa39038985b6e8ad6aa4baee0b74c422'
auth_token = 'a07e8e593d0fc86c5998faccf3661695'
client = Client(account_sid, auth_token)


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.mount("/templates", StaticFiles(directory="templates"), name="static")
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    text : str
    
@app.post('/chat')
async def chat(request: Request):
    data = await request.form()
    twiml_response = MessagingResponse()
    twiml_response.message(get_response(data.get("Body")))
    return Response(content=str(twiml_response), media_type='application/xml')

def get_response(query: str):
    return server.get_answer(query)
    
@app.post('/kutty')
async def chat(item : Item):
    return get_response(item.text)

@app.post("/upload")
async def upload_audio(audio: UploadFile = File(...)):
    # Here, you can process the uploaded audio file as needed
    # For example, you could save it to a specific location
    # and return a response with the URL to the saved audio file
    return {"message": "Audio uploaded successfully"}
    
@app.get("/")
async def read_root(request: Request):
    # get file from form
    return templates.TemplateResponse("index.html", {"request": request})
    

if __name__ == "__main__":
    server = Server()
    server.load_pinecone()
    uvicorn.run(app, port=8000)