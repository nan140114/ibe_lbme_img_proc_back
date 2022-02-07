import os
from typing import Optional, Any
from pydantic import BaseModel
from google.cloud import datastore
from utils.datastore import datastore_client
from google.cloud import storage
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
        return image.key.id
    
    def save_image_to_private_bucket(self, image_id):
        metadata = { "image_id" : image_id }
        client         = storage.Client(project=os.environ["PROJECT_ID"])
        private_bucket = client.get_bucket(constants.PRIVATE_BUCKET_NAME)
        new_image = private_bucket.blob(f'{self.filename}')
        new_image.metadata = metadata
        print(self.filename)
        new_image.upload_from_filename(filename=self.local_path)

    def save(self):
        self.create_local_file()
        image_id = self.save_on_db()
        self.save_image_to_private_bucket(image_id)