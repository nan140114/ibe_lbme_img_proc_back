import os
from google.cloud import storage
from config import constants

client         = storage.Client(project=os.environ["PROJECT_ID"])
private_bucket = client.get_bucket(constants.PRIVATE_BUCKET_NAME)

def save_image_to_private(local_path):
    print(local_path)
    print(local_path.split("/"))
    filename = local_path.split("/")[2]
    new_file = private_bucket.blob(f'{filename}')
    new_file.upload_from_filename(filename=local_path)