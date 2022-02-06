import os
from google.cloud import datastore

def datastore_client():
    return datastore.Client(project=os.environ["PROJECT_ID"])