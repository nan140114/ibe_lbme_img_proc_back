import os

try:
    ENV        = os.environ["ENV"]
    PROJECT    = os.environ["PROJECT_ID"] 
except ValueError:
    print("Not environment variable set. Unable to read buckets")

PUBLIC_BUCKET_NAME  =  f'{ENV}-{PROJECT}-public-images-bucket'
PRIVATE_BUCKET_NAME =  f'{ENV}-{PROJECT}-private-images-bucket'
SUPPORTED_MIME_TYPES = ["image/svg+xml", "image/png", "image/jpeg"," image/gif"]