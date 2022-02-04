from fastapi import FastAPI, File, Form, UploadFile
from utils import create_temp_file, get_image_attr

app = FastAPI()

tmp_path="/tmp/"

@app.get("/")
def get_images():
    return {"message": "Hello world!"}

@app.post("/")
def create_upload_file(uploaded_file: UploadFile):
    tmp_file_path = create_temp_file(uploaded_file.file.read())
    return get_image_attr(tmp_file_path)