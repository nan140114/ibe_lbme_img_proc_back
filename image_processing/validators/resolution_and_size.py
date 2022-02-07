import os
import tempfile
from PIL import Image
from google.cloud import storage
from pathlib import Path
from google.cloud import datastore
from config.constants import CONDITION_TO_VALIDATE, SUPPORTED_WIDTH, SUPPORTED_SIZE, SUPPORTED_HEIGTH

def update_image(image_id, width, heigth, size, is_valid):
    client = datastore.Client(project=os.environ["PROJECT_ID"])
    with client.transaction():
        key = client.key('Images', int(image_id))
        image = client.get(key)
        # iterate through the entity to take over all existing property values
        for prop in image:
            image[prop] = image[prop]
        image["width"]    = width
        image["heigth"]   = heigth
        image["valid"] = is_valid
        image["size"] = size
        client.put(image)
    return image.key.id

def validate_conditions(width, heigth, size):
    if  CONDITION_TO_VALIDATE == "==":
        return  SUPPORTED_HEIGTH == heigth and SUPPORTED_WIDTH == width and SUPPORTED_SIZE == size
    elif  CONDITION_TO_VALIDATE == "<":
        return  heigth < SUPPORTED_HEIGTH and width  < SUPPORTED_WIDTH and size  < SUPPORTED_SIZE
    elif  CONDITION_TO_VALIDATE == "<=":
        return  heigth <= SUPPORTED_HEIGTH and width  <= SUPPORTED_WIDTH and size <= SUPPORTED_SIZE
    elif  CONDITION_TO_VALIDATE == ">=":
        return  heigth >= SUPPORTED_HEIGTH and width  >= SUPPORTED_WIDTH and size  >= SUPPORTED_SIZE
    elif  CONDITION_TO_VALIDATE == ">":
        return  heigth > SUPPORTED_HEIGTH and width  > SUPPORTED_WIDTH and size  > SUPPORTED_SIZE

def validate_size_and_resolution(bucket, filename):
    client          = storage.Client(project=os.environ["PROJECT_ID"])
    temp_local_path = tempfile.NamedTemporaryFile().name
    blob            = client.bucket(bucket).get_blob(filename)
    blob.download_to_filename(temp_local_path)
    image_id = blob.metadata["image_id"]
    image = Image.open(temp_local_path)
    width, heigth = image.size
    size     = Path(temp_local_path).stat().st_size
    is_valid = validate_conditions(width, heigth, size)
    update_image(image_id, width, heigth, size, is_valid)

