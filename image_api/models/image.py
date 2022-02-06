import os
from typing import Optional, Any
from pydantic import BaseModel
from google.cloud import datastore
from utils.datastore import datastore_client
from config import constants
import tempfile

class Image(BaseModel):
    filename   : Optional[str]
    bucket     : Optional[str]  = constants.PRIVATE_BUCKET_NAME
    width      : Optional[int]  = 0
    heigth     : Optional[int]  = 0
    is_valid   : Optional[bool] = False
    public     : Optional[bool] = False
    local_path : Optional[str]
    content    : Any

    def create_local_file(self):
        self.local_path = tempfile.NamedTemporaryFile().name
        self.filename   = self.local_path.split("/")[2]
        with open(self.local_path, "wb+") as file_object:
            file_object.write(self.content)

    def save_on_db(self):
        client = datastore_client()
        image = datastore.Entity(client.key("Images"))
        image.update({
                "filename" : self.filename,
                "bucket"   : self.bucket,
                "width"    : self.width,
                "heigth"   : self.heigth,
                "is_valid" : self.is_valid,
                "public"   : self.public,
        })
        client.put(image)

    def save(self):
        self.create_local_file()
        self.save_on_db()