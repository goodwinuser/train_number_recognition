from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
import random
import datetime
from fastapi.openapi.docs import get_swagger_ui_html
import number_detecting


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/docs")
def read_docs():
    return get_swagger_ui_html(title='title', openapi_url="/openapi.json")

@app.post("/api")
def upload(file: UploadFile = File(...)):

    
    result = {}
    result['is_completed'] = True
    result['numbers']= number_detecting.recognize__digits(file)
    result["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    return result


