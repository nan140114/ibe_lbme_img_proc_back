
from PIL import Image
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, Request

app = FastAPI()

@app.post("/validate")
async def get_image_attr(request: Request):
    # image = Image.open(file_location)
    # width, height = image.size
    # file_size = Path(file_location).stat().st_size
    # return {
    #     "size"      : file_size,
    #     "size_unit" : "bytes",
    #     "width"     : width,
    #     "height"    : height 
    # }
    print(await request.body())
    return {"status" : 200}