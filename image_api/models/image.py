import os
from typing import Optional, Any
from pydantic import BaseModel
from google.cloud import datastore
from utils.datastore import datastore_client, clean_queries
from utils.storage import move_image_to_public_bucket
from google.cloud import storage
from config import constants
import tempfile
import json

class Image(BaseModel):
    filename   : Optional[str]  = ""
    bucket     : Optional[str]  = constants.PRIVATE_BUCKET_NAME
    width      : Optional[int]  = 0
    heigth     : Optional[int]  = 0
    valid      : Optional[bool] = False
    public     : Optional[bool] = False
    local_path : Optional[str]  = ""
    content    : Any
    user_id    : Optional[int]  = 0
    original_filename    : Optional[str]  = ""

    @staticmethod
    def get_all(public=True):
        client = datastore_client()
        all_images = client.query(kind="Images")
        if public:
            all_images.add_filter("public", "=" , public)
        print(list(all_images.fetch()))
        all_images = map( clean_queries , list(all_images.fetch()) )
        return list(all_images)

    @staticmethod
    def get_images_by_user(user_id):
        client = datastore_client()
        filtered_images = client.query(kind="Images")
        filtered_images.add_filter("user_id", "=" , int(user_id))
        filtered_images.add_filter("public",  "=" , False)
        filtered_images = map( clean_queries , list(filtered_images.fetch()) )
        return list(filtered_images)

    def create_local_file(self):
        self.local_path = f"{tempfile.NamedTemporaryFile().name}.{self.original_filename.split('.')[1]}"
        self.filename   = self.local_path.split("/")[2]
        with open(self.local_path, "wb+") as file_object:
            file_object.write(self.content)
    
    @staticmethod
    def make_public(image_id):
        client = datastore_client()
        print(image_id)
        private_bucket = constants.PRIVATE_BUCKET_NAME
        public_bucket  = constants.PUBLIC_BUCKET_NAME 
        with client.transaction():
            key = client.key('Images', int(image_id))
            image = client.get(key)
            print(str(image["filename"]))
            move_image_to_public_bucket(private_bucket, str(image["filename"]), public_bucket)
            image["public"] = True
            image["bucket"] = public_bucket
            client.put(image)
        return image.key.id


    def save_on_db(self):
        client = datastore_client()
        image = datastore.Entity(
            client.key("Images"),
            exclude_from_indexes=("width", "heigth", "size" )
        )
        image.update({
            "filename" : f"{self.filename}",
            "bucket"   : self.bucket,
            "width"    : self.width,
            "heigth"   : self.heigth,
            "valid"    : self.valid,
            "public"   : self.public,
            "user_id"  : self.user_id,
            "original_filename"  : self.original_filename
        })
        print(dict(image))
        client.put(image)
        return image.key.id
    
    def save_image_to_private_bucket(self, image_id):
        metadata = { "contentType": "image/jpeg", "image_id" : image_id }
        client         = storage.Client(project=os.environ["PROJECT_ID"])
        private_bucket = client.get_bucket(constants.PRIVATE_BUCKET_NAME)
        new_image = private_bucket.blob(f'{self.filename}')
        new_image.metadata = metadata
        new_image.content_type = 'image/jpeg'
        print(self.filename)
        new_image.upload_from_filename(filename=self.local_path)

    def save(self):
        self.create_local_file()
        image_id = self.save_on_db()
        self.save_image_to_private_bucket(image_id)