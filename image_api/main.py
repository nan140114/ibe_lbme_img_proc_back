from fastapi import FastAPI, File, Form, UploadFile
from utils.files import create_temp_file, get_image_attr
from utils.storage import save_image_to_private
from models.image import Image

app = FastAPI()

@app.get("/images")
def get_all_images():
    print("get /images")
    return {
        "from": "get_images",
        "status": 200
    }

@app.post("/images")
def new_image(uploaded_file: UploadFile):
    print("post /images")
    image_data = { "content" : uploaded_file.file.read() }
    img = Image(**image_data)
    img.save()
    return {
        "from": "post_image",
        "status": 200
    }

@app.post("/images/{image_id}")
def new_image(uploaded_file: UploadFile):
    return {
        "from": "post_arg_image",
        "status": 200
    }

@app.get("/images/{image_id}")
def new_image(image_id):
    return {
        "from": "get_arg_image",
        "status": 200
    }
