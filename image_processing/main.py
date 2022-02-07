
from PIL import Image
from fastapi import FastAPI, File, Form, UploadFile, Request
from validators.resolution_and_size import validate_size_and_resolution

app = FastAPI()

@app.post("/validate")
async def get_image_attr(request: Request):
    try:
        request_data = await request.json()
        if request_data["message"]["attributes"]["action"] == "analyze":
            image_filename = request_data["message"]["attributes"]["objectId"]
            image_bucket   = request_data["message"]["attributes"]["bucketId"]
            validate_size_and_resolution(image_bucket, image_filename)
    except RuntimeError:
        data = "Failed to get request data"

    return {"status" : 200}
