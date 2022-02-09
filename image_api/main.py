from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from utils.files import create_temp_file, get_image_attr
from utils.storage import save_image_to_private
from models.image import Image
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from config.constants import SUPPORTED_MIME_TYPES
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/images")
def get_all_images():
    all_images = Image.get_all()
    return all_images

@app.get("/images/user/{user_id}")
def filter_images_by_user(user_id: int):
    print(user_id)
    filtered_images = Image.get_images_by_user(user_id)
    return filtered_images

@app.post("/images")
def new_image(uploaded_file: UploadFile, user_id: int):
    image_data = { 
        "user_id": user_id,
        "content" : uploaded_file.file.read(),
        "original_filename": uploaded_file.filename
    }
    print(uploaded_file.content_type)
    if uploaded_file.content_type in SUPPORTED_MIME_TYPES:
        image = Image(**image_data)
        image.save()
        return {
            "status_code": 200,
            "details": "The image has been successfully created"
        }
    else:
        raise HTTPException(status_code=404, detail="The file type isn't supported")


@app.post("/images/{image_id}/publish")
def make_image_public(image_id):
    Image.make_public(image_id)
    return {
        "status_code": 200,
        "details": "The image has been successfully published"
    }
