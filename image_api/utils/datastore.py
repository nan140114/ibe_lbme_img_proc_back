import os
from google.cloud import datastore

def datastore_client():
    return datastore.Client(project=os.environ["PROJECT_ID"])

def clean_queries(image_entity):
    print(image_entity.key.id)
    print(dict(image_entity))
    image_object = dict(image_entity)
    image_object["id"] = image_entity.key.id
    return image_object