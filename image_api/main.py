from fastapi import FastAPI, File, Form, UploadFile
from utils.files import create_temp_file, get_image_attr
from utils.storage import save_image_to_private
from models.image import Image
import json

app = FastAPI()

@app.get("/images")
def get_all_images():
    all_images = Image.get_all()
    return all_images

@app.post("/images")
def new_image(uploaded_file: UploadFile, user_id: int):
    print("post /images")
    print(user_id)
    image_data = { "content" : uploaded_file.file.read() }
    image = Image(**image_data)
    image.save()
    return {
        "status": 200
    }

@app.post("/images/{image_id}")
def edit_image(image_id, image: Image):
    print(image)
    print(image_id)

@app.get("/images/{image_id}")
def new_image(image_id):
    return {
        "status": 200
    }
