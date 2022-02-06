from fastapi import FastAPI, File, Form, UploadFile
from utils.files import create_temp_file, get_image_attr
from utils.storage import save_image_to_private
from models.image import Image

app = FastAPI()

@app.get("/images")
def get_all_images():
    return {"message": "Hello world!"}

@app.post("/images")
def new_image(uploaded_file: UploadFile):
    image_data = { "content" : uploaded_file.file.read() }
    img = Image(**image_data)
    img.save()
    return {"status": 200}

@app.post("/images/{image_id}")
def new_image(uploaded_file: UploadFile):
    return {"status": 200}

@app.get("/images/{image_id}")
def new_image(image_id):
    return {"status": 200}
