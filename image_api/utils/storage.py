import os
from google.cloud import storage
from config import constants

client         = storage.Client(project=os.environ["PROJECT_ID"])


def save_image_to_private(local_path):
    print(local_path)
    print(local_path.split("/"))
    private_bucket = client.get_bucket(constants.PRIVATE_BUCKET_NAME)
    filename = local_path.split("/")[2]
    new_file = private_bucket.blob(f'{filename}')
    new_file.upload_from_filename(filename=local_path)

def move_image_to_public_bucket(private_bucket, private_filename, public_bucket):
    source_bucket = client.get_bucket(private_bucket)
    source_blob = source_bucket.blob(private_filename)
    destination_bucket = client.get_bucket(public_bucket)

    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, private_filename)
    # delete in old destination
    source_blob.delete()